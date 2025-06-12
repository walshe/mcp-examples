from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# mcp_client.py
"""
This script acts as a client for interacting with an MCP (Model Context Protocol) server implementation.

It launches the reference Binance MCP server implementation as a subprocess using stdio, then connects to it using the MCP client protocol.

Key steps:
- Defines the root and MCP server folder paths.
- Configures the server parameters to launch the MCP server (binance_mcp.py) via Python.
- Uses `stdio_client` to start the server and establish a communication channel.
- Creates a `ClientSession` to manage the MCP protocol session.
- Initializes the session and calls the `get_price` tool on the server, passing a symbol (BTCUSDXXX) as an argument.
- Prints the result of the tool call.

This script is intended as a minimal example for interacting with an MCP server using the provided Python client libraries.
"""

ROOT_FOLDER = Path(__file__).parent.absolute()
MCP_FOLDER = ROOT_FOLDER / "binance_mcp_reference_implementation"

server_params = StdioServerParameters(
    command="python",  # Executable
    args=[str(MCP_FOLDER / "binance_mcp.py")],
    env=None,
)


async def run():
    """
    Launches the MCP server as a subprocess and interacts with it using the MCP client protocol.

    Steps:
    - Starts the MCP server using stdio communication.
    - Establishes a client session for protocol communication.
    - Initializes the session (performs handshake/setup).
    - Calls the 'get_price' tool on the server with a hardcoded symbol ('BTCUSDXXX').
    - Prints the result returned by the server.
    """
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "get_price", arguments={"symbol": "BTCUSDT"}
            )
            print(result)


if __name__ == "__main__":
    import asyncio

    # Run the async client entrypoint
    asyncio.run(run())
