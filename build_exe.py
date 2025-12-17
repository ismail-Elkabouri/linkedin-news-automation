#!/usr/bin/env python3
"""
Build script to create LINK.exe standalone application
Run this script to generate the executable
"""

import subprocess
import os
import shutil
import sys

def build_exe():
    """Build the executable using PyInstaller"""
    
    print("=" * 60)
    print("LINK App - Building Executable")
    print("=" * 60)
    
    # PyInstaller command with proper PyQt5 support
    cmd = [
        'pyinstaller',
        '--onefile',  # Single executable file
        '--windowed',  # No console window
        '--name=LINK',  # Output name
        '--hidden-import=PyQt5',  # PyQt5 support
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--distpath=./dist',
        '--workpath=./build',
        '--specpath=./build',
        'gui_app.py'
    ]
    
    try:
        print("\nBuilding executable...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Executable built successfully!")
            print("\nOutput:")
            print(result.stdout)
            
            # Copy to root for easy access
            if os.path.exists('dist/LINK.exe'):
                shutil.copy('dist/LINK.exe', 'LINK.exe')
                print("\n✓ LINK.exe copied to project root")
                print("  You can now distribute this file!")
            
            return True
        else:
            print("✗ Build failed!")
            print("\nError:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
