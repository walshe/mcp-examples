"""
mcp_with_openai_agent.py

This script demonstrates using an OpenAI agent with the MCP (Model Context Protocol) framework.

Key features:
- Integrates MCP tools with an OpenAI-powered agent for advanced reasoning and tool use.
- Can be used as a reference for building LLM agents that interact with MCP servers.

Typical usage:
- Run as a standalone script to test OpenAI agent workflows with MCP tools.
- Use as a template for more complex agent-based MCP integrations.

See the MCP and OpenAI API documentation for more details on the methods and integration patterns used.
"""

import asyncio
from agents import Agent, Runner, function_tool
from agents.mcp.server import MCPServerSse
from dotenv import load_dotenv
from agents.model_settings import ModelSettings

load_dotenv("../.env")


async def main():
    async with MCPServerSse(
        name="DeepWiki MCP Server",
        params={
            "url": "https://mcp.deepwiki.com/sse",
        },
        client_session_timeout_seconds=30
    ) as mcp_server:
        agent = Agent(
            name="DeepWiki Agent",
            instructions="Use the tools to answer the questions.",
            mcp_servers=[mcp_server],
        )

        prompt = """Take a look at deepwiki and figure out What transport
                    protocols are supported in the 2025-03-26 version of the MCP spec?
                    Using the modelcontextprotocol/python-sdk repo"""


        response = await Runner.run(agent, prompt)
        print(response.final_output)

asyncio.run(main())
