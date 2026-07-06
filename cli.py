import argparse
import asyncio
import sys
import glob
from expense_agent import ExpenseAgent

async def main():
    parser = argparse.ArgumentParser(description="ExpenseAudit Pro CLI")
    parser.add_argument("command", choices=["check-receipt", "check-all-receipts"], help="Command to run")
    parser.add_argument("image_path", nargs="?", help="Path to the receipt image file (required for check-receipt)")
    
    args = parser.parse_args()
    agent = ExpenseAgent()
    
    if args.command == "check-receipt":
        if not args.image_path:
            print("Error: image_path is required for check-receipt")
            sys.exit(1)
        success = await agent.process_expense(args.image_path)
        if not success:
            sys.exit(1)
            
    elif args.command == "check-all-receipts":
        images = glob.glob("*.jpg")
        if not images:
            print("No .jpg files found in the current directory.")
            sys.exit(0)
            
        print(f"===============================================")
        print(f"Found {len(images)} receipts to process. Starting batch job...")
        print(f"===============================================\n")
        
        for img in images:
            print(f"===============================================")
            print(f"Processing: {img}")
            print(f"===============================================")
            await agent.process_expense(img)
            print("\n")

if __name__ == "__main__":
    asyncio.run(main())
