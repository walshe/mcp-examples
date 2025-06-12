"""
price_graph.py

This script demonstrates how to use LangGraph and LangChain to build a graph-based agent that queries real-time cryptocurrency prices from a Binance MCP server.

Key features:
- Loads environment variables (e.g., API keys) from a .env file.
- Configures and launches a reference MCP server for Binance as a subprocess.
- Uses MultiServerMCPClient to connect to the MCP server and retrieve available tools.
- Sets up a language model (OpenAI or Google Gemini) for agent reasoning.
- Uses LangGraph's create_react_agent to build an agent that can reason and call MCP tools.
- Defines an async function to query the current prices of Bitcoin and Ethereum using the agent.
- Prints the agent's answer when run as a script.

Typical usage:
- Run this script to see an example of LLM-driven tool use with MCP and LangGraph.
- Modify the query or agent logic for more advanced workflows or different assets.

Dependencies:
- Requires valid API keys for the selected LLM (OpenAI or Google Gemini) and proper .env configuration.
- Requires the MCP server and all Python dependencies installed.

See the MCP, LangChain, and LangGraph documentation for more details on integration and customization.
"""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI


from langgraph.prebuilt import create_react_agent

load_dotenv()

# For OpenAI, use:
#model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# For Google Gemini, use:
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

ROOT_FOLDER = Path(__file__).parent.parent.absolute()
MCP_PATH = str(ROOT_FOLDER / "binance_mcp_reference_implementation" / "binance_mcp.py")

mcp_config = {
    "binance": {
        "command": "python",
        "args": [MCP_PATH],
        "transport": "stdio",
    }
}


async def get_crypto_prices():
    async with MultiServerMCPClient(mcp_config) as client:
        tools = client.get_tools()

        agent = create_react_agent(model, tools)

        query = "What are the current prices of Bitcoin and Ethereum?"
        message = HumanMessage(content=query)

        response = await agent.ainvoke({"messages": [message]})

        answer = response["messages"][-1].content

        return answer


if __name__ == "__main__":
    # Run the main async function
    response = asyncio.run(get_crypto_prices())
    print(response)
