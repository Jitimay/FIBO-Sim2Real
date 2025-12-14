#!/usr/bin/env python3
"""
Launch the FIBO-Sim2Real Factory server
"""
import uvicorn
from backend.main import app

if __name__ == "__main__":
    print("🚀 Starting FIBO-Sim2Real Factory Server...")
    print("📱 Web UI: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
