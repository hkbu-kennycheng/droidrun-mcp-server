# DroidRun MCP Server

A text-based MCP (Model Context Protocol) server for controlling Android devices from Claude Code. Pure accessibility tree automation - no screenshots needed.

## Features

- **Text-based UI interaction** - Read and interact with Android UI elements using accessibility tree
- **No screenshots required** - Faster and more efficient than vision-based approaches
- **Simple indexed tapping** - Elements are numbered for easy interaction
- **Full device control** - Navigate, type, swipe, and launch apps

## Prerequisites

- **Android device** with USB debugging enabled
- **Python 3.10+**
- **ADB (Android Debug Bridge)** installed on your computer
- **Claude Code CLI** installed

---

## Step 1: Install ADB

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install adb
```

### macOS
```bash
brew install android-platform-tools
```

### Windows
Download from [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools) and add to PATH.

---

## Step 2: Enable USB Debugging on Android

1. Go to **Settings > About Phone**
2. Tap **Build Number** 7 times to enable Developer Options
3. Go back to **Settings > System > Developer Options**
4. Enable **USB Debugging**
5. Connect your device via USB
6. Accept the "Allow USB debugging" prompt on your phone

Verify connection:
```bash
adb devices
```
You should see your device listed.

---

## Step 3: Install DroidRun

```bash
pip install droidrun
```

### Install DroidRun Portal App on Device

Run the setup command to install the Portal app on your Android device:

```bash
droidrun setup
```

This will:
1. Download the DroidRun Portal APK
2. Install it on your connected device
3. Open the Accessibility Settings

### Enable Accessibility Service

After `droidrun setup`, you need to manually enable the accessibility service:

1. The Accessibility Settings will open automatically
2. Find **DroidRun Portal** in the list
3. Tap on it and **enable the service**
4. Confirm any permission dialogs

You can verify the setup worked:
```bash
droidrun test
```

---

## Step 4: Configure Claude Code (using uvx)

The easiest way to run this MCP server is directly from the GitHub repository using `uvx`, with no manual installation required.

Add the following to your Claude Code configuration (`~/.claude.json`) under `mcpServers`:

```json
{
  "mcpServers": {
    "droidrun": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/hkbu-kennycheng/droidrun-mcp-server",
        "droidrun-mcp"
      ],
      "env": {}
    }
  }
}
```

`uvx` will automatically fetch and run the server from GitHub each time it is invoked.

---

## Alternative: Manual Installation

### Clone the repository

```bash
git clone https://github.com/hkbu-kennycheng/droidrun-mcp-server.git
cd droidrun-mcp-server
```

### Install dependencies

```bash
pip install droidrun mcp
```

---

## Step 5: Configure Claude Code (manual install)

Add the MCP server to your Claude Code configuration.

Edit `~/.claude.json` and add under `mcpServers`:

```json
{
  "mcpServers": {
    "droidrun": {
      "type": "stdio",
      "command": "python3",
      "args": ["/full/path/to/droidrun-mcp-server/server.py"],
      "env": {}
    }
  }
}
```

**Important:** Use the full absolute path to `server.py`!

Example:
```json
{
  "mcpServers": {
    "droidrun": {
      "type": "stdio",
      "command": "python3",
      "args": ["/home/youruser/droidrun-mcp-server/server.py"],
      "env": {}
    }
  }
}
```

### Restart Claude Code

```bash
claude
```

---

## Available Tools

| Tool | Description |
|------|-------------|
| `device_info()` | Get device model, Android version, and serial |
| `ui()` | Get current screen UI elements as indexed list |
| `tap(index)` | Tap element by index number from `ui()` output |
| `tap_xy(x, y)` | Tap screen at specific coordinates |
| `swipe(direction)` | Swipe up/down/left/right |
| `text(content)` | Input text (optionally tap element first) |
| `back()` | Press Android back button |
| `home()` | Press Android home button |
| `enter()` | Press Enter key |
| `app(package)` | Open app by package name |
| `apps()` | List installed apps (non-system) |

---

## Usage Example

Once configured, you can ask Claude Code to control your Android device:

```
> Open the Settings app and go to About Phone

Claude will:
1. Call app("com.android.settings")
2. Call ui() to see the screen
3. Call tap() on the appropriate elements
4. Navigate to About Phone
```

Example `ui()` output:
```
APP: Settings (com.android.settings)
KEYBOARD: hidden
FOCUS: none

1. TextView: "Network & internet" - (0,200,1080,300)
2. TextView: "Connected devices" - (0,300,1080,400)
3. TextView: "Apps" - (0,400,1080,500)
4. TextView: "About phone" - (0,900,1080,1000)
```

Then Claude taps element 4: `tap(4)`

---

## How It Works

This MCP server wraps the [DroidRun](https://github.com/droidrun/droidrun) library to provide Android device control through Claude Code. It uses the Android accessibility tree (not screenshots) for UI detection, making it fast and reliable.

The DroidRun Portal app runs on your Android device and provides:
- Accessibility service for UI tree extraction
- Numbered overlay for visual feedback (optional)
- Input method for text entry

---

## Troubleshooting

### "No Android device connected"
```bash
# Check if device is connected
adb devices

# If not listed, try:
adb kill-server
adb start-server
adb devices
```

### "Portal is not installed"
```bash
droidrun setup
```

### "Accessibility service not enabled"
1. Go to **Settings > Accessibility**
2. Find **DroidRun Portal**
3. Enable the service

Or run `droidrun setup` again - it will open the settings for you.

### MCP server not showing in Claude Code
1. Check your `~/.claude.json` configuration
2. Ensure the path to `server.py` is **absolute** (starts with `/`)
3. Restart Claude Code completely after config changes

### "Permission denied" errors
Make sure `server.py` is executable:
```bash
chmod +x server.py
```

---

## Quick Start Summary

```bash
# 1. Install ADB
sudo apt install adb  # Linux

# 2. Enable USB debugging on your Android device

# 3. Connect device and verify
adb devices

# 4. Install DroidRun
pip install droidrun

# 5. Setup Portal app on device
droidrun setup

# 6. Enable accessibility service on device (manual step!)

# 7. Add to ~/.claude.json using uvx (recommended):
# {
#   "mcpServers": {
#     "droidrun": {
#       "type": "stdio",
#       "command": "uvx",
#       "args": ["--from", "git+https://github.com/hkbu-kennycheng/droidrun-mcp-server", "droidrun-mcp"]
#     }
#   }
# }

# 8. Restart Claude Code
claude
```

---

## License

MIT

## Credits

- [DroidRun](https://github.com/droidrun/droidrun) - Android automation framework
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol by Anthropic
