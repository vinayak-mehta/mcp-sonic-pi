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
async def initialize_sonic_pi() -> str:
    """Initialize the Sonic Pi server

    Returns:
        The system prompt for the server
    """
    if not check_sonic_pi_running():
        return "Error: Sonic Pi does not appear to be running. Please start Sonic Pi first."

    if not PSONIC_AVAILABLE:
        return (
            "Error: The psonic library couldn't be initialized. Check Sonic Pi status."
        )

    try:
        set_server_parameter_from_log("127.0.0.1")
        return system_prompt()
    except Exception as e:
        return f"Error initializing server: {str(e)}"


@mcp.tool()
async def play_music(code: str) -> str:
    """Play music using Sonic Pi code.

    Args:
        code: Sonic Pi Ruby code

    Returns:
        A confirmation message
    """
    if not check_sonic_pi_running():
        return "Error: Sonic Pi does not appear to be running. Please start Sonic Pi first."

    if not PSONIC_AVAILABLE:
        return (
            "Error: The psonic library couldn't be initialized. Check Sonic Pi status."
        )

    try:
        stop()
        run(code)
        send_message("/trigger/prophet", 70, 100, 8)
        return "Code is now running. If you don't hear anything, check Sonic Pi for errors."
    except Exception as e:
        return f"Error running code: {str(e)}"


@mcp.tool()
async def stop_music() -> str:
    """Stop all currently playing Sonic Pi music.

    Returns:
        A confirmation message
    """
    if not check_sonic_pi_running():
        return "Error: Sonic Pi does not appear to be running. Please start Sonic Pi first."

    if not PSONIC_AVAILABLE:
        return (
            "Error: The psonic library couldn't be initialized. Check Sonic Pi status."
        )

    try:
        stop()
        return "Music stopped"
    except Exception as e:
        return f"Error stopping music: {str(e)}"


@mcp.tool()
def get_beat_pattern(style: str) -> str:
    """Get drum beat patterns for Sonic Pi.

    Args:
        style: Beat style (blues, rock, jazz, hiphop, etc.)

    Returns:
        Sonic Pi code for the requested beat pattern
    """
    beats = {
        "blues": """
# Blues Beat
use_bpm 100
swing = 0.15  # Shuffle feel (0 for straight timing)
live_loop :blues_drums do
  sample :hat_tap, amp: 0.9
  sample :drum_bass_hard, amp: 0.9
  sleep 0.5+swing
  sample :hat_tap, amp: 0.7
  sample :drum_bass_hard, amp: 0.8
  sleep 0.5-swing
  sample :drum_snare_hard, amp: 0.8
  sample :hat_tap, amp: 0.8
  sleep 0.5+swing
  sample :hat_tap, amp: 0.7
  sleep 0.5-swing
end
""",
        "rock": """
# Rock Beat
use_bpm 120
live_loop :rock_drums do
  sample :drum_bass_hard, amp: 1
  sample :drum_cymbal_closed, amp: 0.7
  sleep 0.5
  sample :drum_cymbal_closed, amp: 0.7
  sleep 0.5
  sample :drum_snare_hard, amp: 0.9
  sample :drum_cymbal_closed, amp: 0.7
  sleep 0.5
  sample :drum_cymbal_closed, amp: 0.7
  sleep 0.5
end
""",
        "hiphop": """
# Hip-Hop Beat
use_bpm 90
live_loop :hip_hop_drums do
  sample :drum_bass_hard, amp: 1.2
  sleep 1
  sample :drum_snare_hard, amp: 0.9
  sleep 1
  sample :drum_bass_hard, amp: 1.2
  sleep 0.5
  sample :drum_bass_hard, amp: 0.8
  sleep 0.5
  sample :drum_snare_hard, amp: 0.9
  sleep 1
end
""",
        "electronic": """
# Electronic Beat
use_bpm 128
live_loop :electronic_beat do
  sample :bd_haus, amp: 1
  sample :drum_cymbal_closed, amp: 0.3
  sleep 0.5

  sample :drum_cymbal_closed, amp: 0.3
  sleep 0.5

  sample :bd_haus, amp: 0.9
  sample :drum_snare_hard, amp: 0.8
  sample :drum_cymbal_closed, amp: 0.3
  sleep 0.5

  sample :drum_cymbal_closed, amp: 0.3
  sleep 0.5
end
""",
    }

    if style.lower() in beats:
        return beats[style.lower()]
    else:
        return f"Beat style '{style}' not found. Available styles: {', '.join(beats.keys())}"


@mcp.prompt()
def system_prompt():
    return """
    You are a Sonic Pi assistant that helps users create musical compositions using code. Your knowledge includes various rhythm patterns, chord progressions, scales, and proper Sonic Pi syntax. Respond with accurate, executable Sonic Pi code based on user requests. Remember to call initialize_sonic_pi first before playing any music with Sonic Pi.

    You can use chords to create progressions. Chords have the following format: chord  tonic (symbol), name (symbol)

    Here's an example chord with C tonic and various names:
    (chord :C, '1')
    (chord :C, '5')
    (chord :C, '+5')
    (chord :C, 'm+5')
    (chord :C, :sus2)
    (chord :C, :sus4)
    (chord :C, '6')
    (chord :C, :m6)
    (chord :C, '7sus2')
    (chord :C, '7sus4')
    (chord :C, '7-5')
    (chord :C, 'm7-5')
    (chord :C, '7+5')
    (chord :C, 'm7+5')
    (chord :C, '9')
    (chord :C, :m9)
    (chord :C, 'm7+9')
    (chord :C, :maj9)
    (chord :C, '9sus4')
    (chord :C, '6*9')
    (chord :C, 'm6*9')
    (chord :C, '7-9')
    (chord :C, 'm7-9')
    (chord :C, '7-10')
    (chord :C, '9+5')
    (chord :C, 'm9+5')
    (chord :C, '7+5-9')
    (chord :C, 'm7+5-9')
    (chord :C, '11')
    (chord :C, :m11)
    (chord :C, :maj11)
    (chord :C, '11+')
    (chord :C, 'm11+')
    (chord :C, '13')
    (chord :C, :m13)
    (chord :C, :add2)
    (chord :C, :add4)
    (chord :C, :add9)
    (chord :C, :add11)
    (chord :C, :add13)
    (chord :C, :madd2)
    (chord :C, :madd4)
    (chord :C, :madd9)
    (chord :C, :madd11)
    (chord :C, :madd13)
    (chord :C, :major)
    (chord :C, :M)
    (chord :C, :minor)
    (chord :C, :m)
    (chord :C, :major7)
    (chord :C, :dom7)
    (chord :C, '7')
    (chord :C, :M7)
    (chord :C, :minor7)
    (chord :C, :m7)
    (chord :C, :augmented)
    (chord :C, :a)
    (chord :C, :diminished)
    (chord :C, :dim)
    (chord :C, :i)
    (chord :C, :diminished7)
    (chord :C, :dim7)
    (chord :C, :i7)

    Remember that all Sonic Pi code must be valid Ruby code, with proper indentation, parameter passing, and loop definitions. When composing patterns, always ensure the timing adds up correctly within each loop.
"""


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
