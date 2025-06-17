# Create server parameters for stdio connection
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langsmith import traceable, tracing_context


@traceable(run_type="chain", name="Notion with Adapter", project_name="Promblem-first-ai-demo")
async def main():
    model = ChatOpenAI(model="gpt-4o")

    server_params = StdioServerParameters(
        command="python",
        # Make sure to update to the full absolute path to your math_server.py file
        args=[
            "/Users/gman/Documents/Problem-First/external-mcp-server/server/notionserver.py"
        ],
    )
   
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke(
                {"messages": "Add change AC filter to my list on TODO page in Notion if it is not already there and fetch the list of items from the page."},
            )

            print(agent_response.get('messages')[-1].content)


if __name__ == "__main__":
    asyncio.run(main())
