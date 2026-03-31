#!/usr/bin/env python3
"""
DroidRun MCP Server - Text-based Android control for Claude Code
Pure accessibility tree automation, no screenshots needed.
"""

import asyncio
import logging
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Configure logging to stderr (not stdout)
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("droidrun")

# Global tools instance
_tools = None
_serial = None


async def get_tools():
    """Get or create the AdbTools instance."""
    global _tools, _serial

    if _tools is None:
        from droidrun.tools.adb import AdbTools
        from async_adbutils import adb

        devices = await adb.list()
        if not devices:
            raise Exception("No Android device connected")

        _serial = devices[0].serial
        # vision_enabled=False for detailed text output
        _tools = AdbTools(serial=_serial, vision_enabled=False)
        await _tools.connect()

    return _tools


@mcp.tool()
async def device_info() -> str:
    """Get basic device information (model, Android version)."""
    from async_adbutils import adb

    devices = await adb.list()
    if not devices:
        return "ERROR: No device connected"

    device = await adb.device(serial=devices[0].serial)
    model = (await device.shell("getprop ro.product.model")).strip()
    android = (await device.shell("getprop ro.build.version.release")).strip()

    return f"Model: {model} | Android: {android} | Serial: {devices[0].serial}"


@mcp.tool()
async def ui() -> str:
    """Get current screen UI elements. Returns indexed list of interactive elements.
    Use the index numbers with tap() to interact with elements."""
    tools = await get_tools()

    formatted_text, focused_text, _, phone_state = await tools.get_state()

    return f"""APP: {phone_state.get('currentApp', '?')} ({phone_state.get('packageName', '?')})
KEYBOARD: {'visible' if phone_state.get('keyboardVisible') else 'hidden'}
FOCUS: {focused_text or 'none'}

{formatted_text}"""


@mcp.tool()
async def tap(index: int) -> str:
    """Tap UI element by index number from ui() output.

    Args:
        index: Element index to tap
    """
    tools = await get_tools()
    return await tools.tap(index)


@mcp.tool()
async def tap_xy(x: int, y: int) -> str:
    """Tap screen at coordinates.

    Args:
        x: X coordinate
        y: Y coordinate
    """
    tools = await get_tools()
    success = await tools.tap_by_coordinates(x, y)
    return f"Tap ({x},{y}): {'OK' if success else 'FAILED'}"


@mcp.tool()
async def swipe(direction: str, duration_ms: int = 500) -> str:
    """Swipe in a direction.

    Args:
        direction: up, down, left, or right
        duration_ms: Swipe duration in ms (default 500)
    """
    tools = await get_tools()

    # Screen center and swipe distances
    cx, cy = 540, 1200
    dist = 600

    coords = {
        "up": (cx, cy + dist, cx, cy - dist),
        "down": (cx, cy - dist, cx, cy + dist),
        "left": (cx + dist, cy, cx - dist, cy),
        "right": (cx - dist, cy, cx + dist, cy),
    }

    if direction not in coords:
        return f"ERROR: direction must be up/down/left/right"

    x1, y1, x2, y2 = coords[direction]
    success = await tools.swipe(x1, y1, x2, y2, duration_ms)
    return f"Swipe {direction}: {'OK' if success else 'FAILED'}"


@mcp.tool()
async def text(content: str, index: int = -1, clear: bool = False) -> str:
    """Input text. Optionally tap element first.

    Args:
        content: Text to type
        index: Element index to tap first (-1 to skip)
        clear: Clear existing text first
    """
    tools = await get_tools()
    return await tools.input_text(content, index=index, clear=clear)


@mcp.tool()
async def back() -> str:
    """Press Android back button."""
    tools = await get_tools()
    return await tools.back()


@mcp.tool()
async def home() -> str:
    """Press Android home button."""
    tools = await get_tools()
    return await tools.press_key(3)


@mcp.tool()
async def enter() -> str:
    """Press Enter key."""
    tools = await get_tools()
    return await tools.press_key(66)


@mcp.tool()
async def app(package: str) -> str:
    """Open app by package name.

    Args:
        package: Package name (e.g. com.android.settings)
    """
    tools = await get_tools()
    return await tools.start_app(package)


@mcp.tool()
async def apps() -> str:
    """List installed apps (non-system)."""
    tools = await get_tools()
    packages = await tools.list_packages(include_system_apps=False)
    return f"Apps ({len(packages)}):\n" + "\n".join(sorted(packages)[:30])


def main():
    mcp.run()


if __name__ == "__main__":
    main()
