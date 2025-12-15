#!/usr/bin/env python3
"""
Enhanced server startup script with diagnostics
"""
import sys
import os
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'requests',
        'pillow',
        'opencv-python',
        'numpy',
        'ultralytics',
        'torch',
        'python-dotenv',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    return missing_packages

def check_directories():
    """Check if required directories exist"""
    required_dirs = [
        'backend',
        'frontend',
        'uploads',
        'dataset',
        'models',
        'results'
    ]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/")
        else:
            print(f"⚠️  {dir_name}/ - Creating...")
            dir_path.mkdir(exist_ok=True)

def check_files():
    """Check if required files exist"""
    required_files = [
        'backend/main_standalone.py',
        'backend/fibo_client.py',
        'backend/dataset_generator.py',
        'backend/model_trainer.py',
        'frontend/index.html',
        'requirements.txt'
    ]
    
    for file_name in required_files:
        file_path = Path(file_name)
        if file_path.exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ {file_name} - MISSING")

def start_server():
    """Start the FastAPI server"""
    try:
        print("🚀 Starting FIBO-Sim2Real Factory Server...")
        
        # Change to backend directory
        backend_dir = Path('backend')
        os.chdir(backend_dir)
        
        # Start the server
        subprocess.run([
            sys.executable, 'main_standalone.py'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    print("🔧 FIBO-Sim2Real Factory - Server Diagnostics")
    print("=" * 50)
    
    print("\n📦 Checking Python packages...")
    missing_packages = check_dependencies()
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("🔧 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return 1
    
    print("\n📁 Checking directories...")
    check_directories()
    
    print("\n📄 Checking files...")
    check_files()
    
    print("\n🚀 All checks passed! Starting server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🌐 Web UI will be available at: http://localhost:8000")
    print("📋 API docs available at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    
    time.sleep(2)
    start_server()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())