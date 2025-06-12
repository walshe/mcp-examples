"""
binance_mcp.py

This script implements a reference MCP (Model Context Protocol) server for Binance price data.

Key features:
- Exposes MCP tools for retrieving price and symbol information from Binance.
- Can be launched as a subprocess and communicates via stdio.
- Used as the backend for MCP client scripts (e.g., mcp_client.py).

Typical usage:
- Run as a standalone MCP server for local development or integration testing.
- Interact with it using an MCP client (see mcp_client.py for an example).

See the MCP protocol and Binance API documentation for more details on the data and methods exposed.
"""

from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Binance MCP")


def get_symbol_from_name(name: str) -> str:
    """
    Convert a human-readable crypto asset name to its Binance symbol.

    Args:
        name (str): The name or symbol of the crypto asset (e.g., 'bitcoin', 'btc', 'ethereum', 'eth').

    Returns:
        str: The Binance trading symbol for the asset (e.g., 'BTCUSDT', 'ETHUSDT').
    """
    if name.lower() in ["bitcoin", "btc"]:
        return "BTCUSDT"
    elif name.lower() in ["ethereum", "eth"]:
        return "ETHUSDT"
    else:
        return name.upper()


@mcp.tool()
def get_price(symbol: str) -> Any:
    """
    Get the current price of a crypto asset from Binance.

    Args:
        symbol (str): The symbol or name of the crypto asset to get the price of.

    Returns:
        Any: The current price of the crypto asset as returned by the Binance API.
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@mcp.tool()
def get_price_price_change(symbol: str) -> Any:
    """
    Get the price change of the last 24 hours of a crypto asset from Binance.

    Args:
        symbol (str): The symbol or name of the crypto asset to get the price change of.

    Returns:
        Any: The price change of the crypto asset in the last 24 hours as returned by the Binance API.
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print("Starting Binance MCP")
    mcp.run(transport="stdio")  # or can be "sse"
