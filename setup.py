#!/usr/bin/env python3
"""
Setup script for FIBO-Sim2Real Factory
"""
import os
import subprocess
import sys

def run_command(cmd):
    """Run shell command and handle errors"""
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running: {cmd}")
        print(f"Error: {e}")
        return False

def main():
    print("🚀 Setting up FIBO-Sim2Real Factory...")
    
    # Create necessary directories
    directories = [
        "uploads", "dataset", "models", "results", 
        "dataset/images/train", "dataset/images/val",
        "dataset/labels/train", "dataset/labels/val"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Install requirements
    print("📦 Installing Python dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("❌ Failed to install dependencies")
        return 1
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("⚠️  No .env file found. Please copy .env.example to .env and add your FIBO API key")
        run_command("cp .env.example .env")
    
    # Make scripts executable
    scripts = [
        "scripts/generate_dataset.py",
        "scripts/train_model.py", 
        "scripts/test_real.py",
        "scripts/export_model.py",
        "edge-demo/edge_inference.py",
        "run_server.py"
    ]
    
    for script in scripts:
        if os.path.exists(script):
            os.chmod(script, 0o755)
            print(f"✅ Made executable: {script}")
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Add your FIBO API key to .env file")
    print("2. Run: python run_server.py")
    print("3. Open: http://localhost:8000")
    print("\n🚀 Ready to generate synthetic datasets!")
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
