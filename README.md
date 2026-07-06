# ExpenseAudit Pro 💼🤖

**Track:** Agents for Business  
**Submission for the Kaggle AI Agents: Intensive Vibe Coding Capstone**

## Overview
ExpenseAudit Pro is an intelligent multi-agent system designed to automate the triage and approval of employee expense reports. It tackles a core business bottleneck: manually reviewing thousands of receipts against complex, dynamic company policies.

Using vision capabilities, the agent reads receipt images, extracts relevant data, **redacts sensitive Personally Identifiable Information (PII)**, and then consults an MCP (Model Context Protocol) Server to check real-time company policies before making an approval decision.

## Hackathon Criteria Addressed

| Requirement | Implementation Detail |
| :--- | :--- |
| **Multi-Agent System** | A Vision/Extraction agent logic coordinates with an Evaluation agent logic to form the decision pipeline. |
| **MCP Server** | `mcp_policy_server.py` acts as an MCP server, securely hosting and serving the company's financial policies to the agent. |
| **Security Features** | The agent explicitly redacts PII (like credit card numbers and names) from the receipt *before* processing the data to ensure compliance. |
| **Deployability** | A `Dockerfile` and `docker-compose.yml` are provided for instant, containerized deployment anywhere. |
| **Agent CLI** | `cli.py` provides a clean command-line interface to interact with the agent. |

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- A Google Gemini API Key

### 2. Installation
Navigate to the project directory and install the requirements:
```bash
pip install -r requirements.txt
```

Create a `.env` file from the template and add your API key:
```bash
cp .env.example .env
# Edit .env and insert your GEMINI_API_KEY
```

### 3. Usage (CLI)
We have included a script to generate a mock receipt for testing:
```bash
python create_mock_receipt.py
```
This will create `receipt.jpg` in your directory.

Run the agent on the receipt:
```bash
python cli.py check-receipt receipt.jpg
```

### 4. Docker Deployment
To run the agent completely within a Docker container:
```bash
# Ensure GEMINI_API_KEY is in your environment or .env file
docker-compose up
```

## How It Works
1. **Vision Extraction**: The agent receives an image and uses `gemini-1.5-flash` to extract the Date, Amount, and Category, while explicitly replacing PII with `[REDACTED]`.
2. **Policy Retrieval**: The agent establishes an MCP connection to the local Policy Server and queries the specific limit for the identified category (e.g., Meals).
3. **Evaluation**: The agent uses `gemini-1.5-pro` to evaluate the extracted amount against the retrieved policy limit and outputs a final Approved/Rejected verdict.
