#!/usr/bin/env python3
"""Take a screenshot from a connected Android phone via ADB and save it locally."""

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def take_screenshot(output_path: str | None = None) -> str:
    device_path = "/sdcard/screenshot.png"

    # Capture screenshot on device
    result = subprocess.run(
        ["adb", "shell", "screencap", "-p", device_path],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f"Failed to capture screenshot: {result.stderr.strip()}")

    # Determine local save path
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/screenshot_{timestamp}.png"

    # Pull file from device
    result = subprocess.run(
        ["adb", "pull", device_path, output_path],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        sys.exit(f"Failed to pull screenshot: {result.stderr.strip()}")

    # Clean up on device
    subprocess.run(["adb", "shell", "rm", device_path], capture_output=True)

    print(f"Screenshot saved to {Path(output_path).resolve()}")
    return output_path


if __name__ == "__main__":
    print("Taking a screenshot every second. Press Ctrl+C to stop.")
    try:
        while True:
            take_screenshot()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped.")
