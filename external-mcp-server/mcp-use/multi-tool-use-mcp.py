import asyncio
import os
import getpass
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp_use import MCPAgent, MCPClient


async def main():
    # Load environment variables
    load_dotenv()

    # -----------------------------

    # Create MCPClient from configuration dictionary
    client = MCPClient.from_config_file(os.path.join("/Users/gman/Documents/Problem-First/mcp-servers/multi-mcp.json"))

    # Create LLM
    llm = ChatOpenAI(model="gpt-4o")

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=60)

    # Run the query
    result = await agent.run(
        """Find the top 2 things to do in Glacier national park and add them to the TODO page in notion.""",
        max_steps=5,
    )
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
