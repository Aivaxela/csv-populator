#!/usr/bin/env python3
"""
Build script to create a standalone Windows executable for CSV Populator
"""

import os
import subprocess
import sys

def build_executable():
    """Build the standalone executable using PyInstaller"""
    
    print("Building standalone Windows executable...")
    
    # PyInstaller command with optimized settings
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (Windows)
        "--name=CSV_Populator",         # Executable name
        "--add-data=README.md;.",       # Include README if it exists
        "--clean",                      # Clean cache
        "--noconfirm",                  # Overwrite output directory
        "csv_populator.py"
    ]
    
    # Remove README flag if it doesn't exist
    if not os.path.exists("README.md"):
        cmd = [arg for arg in cmd if not arg.startswith("--add-data")]
        print("Note: README.md not found, building without README")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print(f"Executable created in: dist/CSV_Populator.exe")
        
        # Show file size
        exe_path = "dist/CSV_Populator.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"File size: {size_mb:.1f} MB")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error code {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print("PyInstaller not found. Please install it first:")
        print("pip install pyinstaller")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

if __name__ == "__main__":
    print("CSV Populator - Executable Builder")
    print("=" * 40)
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("PyInstaller is available")
    except ImportError:
        print("PyInstaller not found. Installing...")
        if not install_dependencies():
            sys.exit(1)
    
    # Build the executable
    if build_executable():
        print("\nBuild completed successfully!")
        print("Your users can now run CSV_Populator.exe without Python installed!")
    else:
        print("\nBuild failed. Please check the error messages above.")
        sys.exit(1)
