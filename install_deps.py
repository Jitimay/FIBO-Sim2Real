#!/usr/bin/env python3
"""
Install missing dependencies for FIBO-Sim2Real Factory
"""
import subprocess
import sys

def run_command(cmd):
    """Run a command and return success status"""
    try:
        print(f"🔧 Running: {cmd}")
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {cmd}")
        print(f"Error: {e.stderr}")
        return False

def install_dependencies():
    print("🚀 Installing FIBO-Sim2Real Factory Dependencies")
    print("=" * 50)
    
    # Essential packages
    packages = [
        "ultralytics",
        "torch",
        "torchvision", 
        "fastapi",
        "uvicorn",
        "python-multipart",
        "pillow",
        "opencv-python",
        "numpy",
        "pyyaml",
        "python-dotenv",
        "requests",
        "tqdm"
    ]
    
    print("📦 Installing packages...")
    
    # Try to install all at once first
    all_packages = " ".join(packages)
    if run_command(f"{sys.executable} -m pip install {all_packages}"):
        print("🎉 All packages installed successfully!")
        return True
    
    # If that fails, try one by one
    print("🔄 Batch install failed, trying individual packages...")
    
    failed_packages = []
    for package in packages:
        if not run_command(f"{sys.executable} -m pip install {package}"):
            failed_packages.append(package)
    
    if failed_packages:
        print(f"\n❌ Failed to install: {', '.join(failed_packages)}")
        print("🔧 Try installing manually:")
        for pkg in failed_packages:
            print(f"   pip install {pkg}")
        return False
    else:
        print("🎉 All packages installed successfully!")
        return True

def verify_installation():
    print("\n🔍 Verifying installation...")
    
    try:
        from ultralytics import YOLO
        print("✅ YOLO/Ultralytics working")
        
        import torch
        print(f"✅ PyTorch {torch.__version__} working")
        
        from fastapi import FastAPI
        print("✅ FastAPI working")
        
        from PIL import Image
        print("✅ Pillow working")
        
        import cv2
        print(f"✅ OpenCV {cv2.__version__} working")
        
        print("\n🎉 All core dependencies verified!")
        return True
        
    except ImportError as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    success = install_dependencies()
    
    if success:
        if verify_installation():
            print("\n🚀 Installation complete! You can now run:")
            print("   python quick_fix_server.py")
        else:
            print("\n⚠️ Installation completed but verification failed")
            print("🔧 Try running: python check_yolo.py")
    else:
        print("\n❌ Installation failed")
        print("🔧 Try manual installation:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()