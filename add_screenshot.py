#!/usr/bin/env python3
"""
Helper script to add screenshot to the repo
Run this after saving your screenshot
"""

import os
import shutil

def add_screenshot():
    """Add screenshot to assets folder and commit"""
    
    assets_dir = "assets"
    screenshot_file = "screenshot-about.png"
    assets_path = os.path.join(assets_dir, screenshot_file)
    
    # Check if file exists
    if not os.path.exists(assets_path):
        print("⚠️  Screenshot not found!")
        print(f"Please save your screenshot as: {assets_path}")
        return False
    
    print(f"✓ Found screenshot: {assets_path}")
    print(f"✓ File size: {os.path.getsize(assets_path) / 1024:.1f} KB")
    
    # Git commands
    print("\nNow run these commands:")
    print("  git add assets/screenshot-about.png")
    print("  git commit -m 'assets: Add LINK app screenshot'")
    print("  git push origin main")
    
    return True

if __name__ == "__main__":
    add_screenshot()
