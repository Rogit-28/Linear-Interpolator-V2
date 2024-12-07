"""
Build script for the Tauri scaling application
"""

import subprocess
import sys
import os
from pathlib import Path

def install_tauri_cli():
    """Install Tauri CLI if not already installed"""
    try:
        result = subprocess.run(["cargo", "install", "tauri-cli"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Tauri CLI installed successfully")
        else:
            print(f"Tauri CLI installation output: {result.stdout}")
            print(f"Tauri CLI installation error: {result.stderr}")
    except FileNotFoundError:
        print("Cargo not found. Please install Rust first.")
        return False
    return True

def build_frontend():
    """Build the Next.js frontend"""
    print("Building frontend...")
    try:
        # Install frontend dependencies
        subprocess.run(["npm", "install"], cwd="frontend/scaling", check=True, shell=True)
        # Build the frontend
        subprocess.run(["npm", "run", "build"], cwd="frontend/scaling", check=True, shell=True)
        print("Frontend built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Frontend build failed: {e}")
        return False

def build_tauri_app():
    """Build the Tauri application"""
    print("Building Tauri app...")
    try:
        # Run tauri build
        result = subprocess.run(["cargo", "tauri", "build", "--release"], 
                              capture_output=True, text=True, check=True)
        print("Tauri app built successfully")
        print(f"Build output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Tauri build failed: {e}")
        print(f"Build error: {e.stderr}")
        return False

def main():
    """Main build function"""
    print("Starting Tauri app build process...")
    
    # Check if Rust is installed
    try:
        subprocess.run(["rustc", "--version"], check=True, capture_output=True)
        print("Rust is installed")
    except FileNotFoundError:
        print("Rust not found. Please install Rust first: https://www.rust-lang.org/tools/install")
        return False
    
    # Install Tauri CLI
    if not install_tauri_cli():
        return False
    
    # Build frontend
    if not build_frontend():
        return False
    
    # Build Tauri app
    if not build_tauri_app():
        return False
    
    print("Build completed successfully! The executable is in src-tauri/target/release/")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
