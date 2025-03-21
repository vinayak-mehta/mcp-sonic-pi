#!/usr/bin/env python3
"""
MCP Server for controlling Sonic Pi via psonic library
"""

import platform
import subprocess

from mcp.server.fastmcp import Context, FastMCP

# Initialize FastMCP server
mcp = FastMCP("sonic-pi")


def check_sonic_pi_running():
    """Check if Sonic Pi is running on the system"""
    system = platform.system()

    if system == "Darwin":  # macOS
        result = subprocess.run(
            ["pgrep", "-x", "Sonic Pi"], capture_output=True, text=True
        )
        return result.returncode == 0

    return False


# Try to import psonic, install if not available
try:
    from psonic import *

    PSONIC_AVAILABLE = True
except Exception as e:
    print(f"Error initializing psonic: {e}")
    PSONIC_AVAILABLE = False


@mcp.tool()
async def initialize(ctx: Context) -> str:
    """Initialize the server"""
    if not check_sonic_pi_running():
        return "Error: Sonic Pi does not appear to be running. Please start Sonic Pi first."

    if not PSONIC_AVAILABLE:
        return (
            "Error: The psonic library couldn't be initialized. Check Sonic Pi status."
        )

    try:
        set_server_parameter_from_log("127.0.0.1")
        return "Server initialized"
    except Exception as e:
        return f"Error initializing server: {str(e)}"


@mcp.tool()
async def play_music(code: str, ctx: Context) -> str:
    """Add and immediately run Sonic Pi code.

    Args:
        code: Sonic Pi Ruby code to run immediately

    Returns:
        A confirmation message
    """
    if not check_sonic_pi_running():
        ctx.warning("Sonic Pi does not appear to be running")
        return "Error: Sonic Pi does not appear to be running. Please start Sonic Pi first."

    if not PSONIC_AVAILABLE:
        ctx.error("psonic library is not properly initialized")
        return (
            "Error: The psonic library couldn't be initialized. Check Sonic Pi status."
        )

    try:
        stop()
        run(code)
        send_message("/trigger/prophet", 70, 100, 8)
        return "Code is now running. If you don't hear anything, check Sonic Pi for errors."
    except Exception as e:
        ctx.error(f"Error running code: {str(e)}")
        return f"Error running code: {str(e)}"


@mcp.tool()
async def stop_music(ctx: Context) -> str:
    """Stop all currently playing Sonic Pi music.

    Returns:
        A confirmation message
    """
    if not check_sonic_pi_running():
        ctx.warning("Sonic Pi does not appear to be running")
        return "Error: Sonic Pi does not appear to be running. Please start Sonic Pi first."

    if not PSONIC_AVAILABLE:
        ctx.error("psonic library is not properly initialized")
        return (
            "Error: The psonic library couldn't be initialized. Check Sonic Pi status."
        )

    try:
        stop()
        return "Music stopped"
    except Exception as e:
        ctx.error(f"Error stopping music: {str(e)}")
        return f"Error stopping music: {str(e)}"


def main():
    if not check_sonic_pi_running():
        print("⚠️ Warning: Sonic Pi doesn't appear to be running")
        print("Please start Sonic Pi before using this MCP server")
    else:
        print("✅ Sonic Pi is running")

    if not PSONIC_AVAILABLE:
        print("⚠️ Warning: psonic library is not properly initialized")
        print("Make sure Sonic Pi is running and log file is accessible")
    else:
        print("✅ psonic library initialized")

    print("Sonic Pi MCP Server initialized")

    # Run the MCP server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
