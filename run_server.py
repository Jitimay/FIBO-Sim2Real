#!/usr/bin/env python3
"""
Server runner for FIBO-Sim2Real Factory
"""
import sys
import os
import uvicorn

def main():
    print("🚀 Starting FIBO-Sim2Real Factory Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🌐 Web UI will be available at: http://localhost:8000")
    print("📋 API docs available at: http://localhost:8000/docs")
    
    try:
        # Add backend directory to Python path
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_dir)
        
        # Import and run the standalone FastAPI app
        from main_standalone import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("🔧 Please check that all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    exit_code = main()
    if exit_code:
        sys.exit(exit_code)