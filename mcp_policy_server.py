from mcp.server.fastmcp import FastMCP
import json
import os

# Initialize FastMCP Server
mcp = FastMCP("ExpensePolicyServer")

def load_policies():
    """Load policies from the local JSON file."""
    policy_file = os.path.join(os.path.dirname(__file__), "policies.json")
    with open(policy_file, "r") as f:
        return json.load(f)["policies"]

@mcp.tool()
def get_expense_policy(category: str) -> str:
    """Get the company expense policy for a specific category (e.g., 'Meals', 'Travel', 'Office Supplies')."""
    policies = load_policies()
    for policy in policies:
        if policy["category"].lower() == category.lower():
            return f"Limit: {policy['limit']} {policy['currency']}. Rules: {policy['rules']}"
    
    return "Policy not found for this category. Please check the category name."

@mcp.tool()
def list_expense_categories() -> list[str]:
    """List all available expense policy categories."""
    policies = load_policies()
    return [p["category"] for p in policies]

if __name__ == "__main__":
    # Run the server using stdio transport (standard for MCP)
    mcp.run(transport='stdio')
