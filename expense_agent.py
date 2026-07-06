import asyncio
import os
import json
import re
import google.generativeai as genai
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

# Initialize Gemini API
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Warning: GEMINI_API_KEY environment variable not set. Please set it in a .env file.")

genai.configure(api_key=api_key)

class ExpenseAgent:
    def __init__(self):
        self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
        self.agent_model = genai.GenerativeModel('gemini-2.5-flash')

    async def _get_policy_from_mcp(self, category: str) -> str:
        """Connects to the local MCP server to fetch policy limits."""
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_policy_server.py"],
            env=None
        )

        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    
                    # Call the get_expense_policy tool provided by our MCP server
                    result = await session.call_tool(
                        "get_expense_policy",
                        arguments={"category": category}
                    )
                    
                    if result and hasattr(result, 'content') and len(result.content) > 0:
                        return result.content[0].text
                    return "Error: Could not retrieve policy content."
        except Exception as e:
            return f"Failed to connect to MCP Server: {e}"

    def _redact_pii_and_extract(self, image_path: str):
        """Uses Vision model to extract data and explicitly redact PII."""
        img = Image.open(image_path)
        prompt = '''
        Analyze this receipt. Extract the following information:
        - Date
        - Category (Must be one of: Meals, Travel, Office Supplies)
        - Total Amount
        
        SECURITY REQUIREMENT: Redact any PII (Personally Identifiable Information) such as Names, Phone Numbers, or Credit Card numbers. Replace them with [REDACTED].
        
        Return the result as a strict JSON object with keys: "date", "category", "total_amount_numeric", "pii_redacted_text".
        '''
        response = self.vision_model.generate_content([prompt, img])
        return response.text

    async def process_expense(self, image_path: str):
        print("1. Scanning receipt and redacting PII...")
        extraction_text = self._redact_pii_and_extract(image_path)
        
        try:
            clean_json = re.sub(r'```json\n|\n```', '', extraction_text).strip()
            data = json.loads(clean_json)
            print(f"Extracted Data: {json.dumps(data, indent=2)}\n")
        except Exception as e:
            print(f"Failed to parse receipt data. Raw output:\n{extraction_text}")
            return False
            
        category = data.get("category", "Unknown")
        amount = data.get("total_amount_numeric", 0)
        
        print(f"2. Querying MCP Policy Server for '{category}'...")
        policy_info = await self._get_policy_from_mcp(category)
        print(f"Policy Info: {policy_info}\n")
        
        print("3. Evaluating compliance...")
        eval_prompt = f'''
        You are an Expense Audit Agent. You have successfully verified the user's receipt.
        
        Expense Amount: {amount}
        Expense Category: {category}
        Company Policy: {policy_info}
        
        Evaluate if this expense should be APPROVED or REJECTED based strictly on the policy.
        Provide a short, definitive explanation.
        '''

        
        evaluation = self.agent_model.generate_content(eval_prompt)
        print(f"\n================ FINAL VERDICT ================\n{evaluation.text}\n===============================================")
        return True
