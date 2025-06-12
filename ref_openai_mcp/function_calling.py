"""
function_calling.py

This script demonstrates function calling with the MCP (Model Context Protocol) framework and OpenAI integration.

Key features:
- Shows how to use MCP tools with OpenAI's function calling capabilities.
- Can be used as a reference for integrating MCP with LLMs that support function/tool calling.

Typical usage:
- Run as a standalone script to test function calling workflows.
- Use as a template for building more advanced MCP + LLM integrations.

See the MCP and OpenAI API documentation for more details on the methods and integration patterns used.
"""

from agents import Agent, Runner, function_tool

from dotenv import load_dotenv

load_dotenv("../.env")


@function_tool
def multiply(x: float, y: float) -> float:
    """
    Multiply two numbers
    """
    return x * y


agent = Agent(
    name="Math Agent",
    instructions="Always use your tools to solve math problems.",
    tools=[multiply],
)

response = Runner.run_sync(agent, "What is 6.2 times 3.5?")
print(response.final_output)
