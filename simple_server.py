#!/usr/bin/env python3
"""
Simplified server for UI testing
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append('backend')
from fibo_client import FIBOClient
from dataset_generator import DatasetGenerator

app = FastAPI(title="FIBO-Sim2Real Factory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
fibo_client = FIBOClient()
dataset_gen = DatasetGenerator(fibo_client)

@app.get("/")
async def serve_ui():
    return FileResponse("frontend/index.html")

@app.post("/upload-golden-image")
async def upload_golden_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(400, "File must be an image")
    
    # Save uploaded image
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    return {"message": "Image uploaded", "path": str(file_path)}

@app.post("/generate-dataset")
async def generate_dataset(request: dict):
    try:
        golden_image_path = request.get("golden_image_path")
        count = request.get("count", 100)
        
        dataset_path = await dataset_gen.generate_synthetic_dataset(
            golden_image_path, count
        )
        return {"message": "Dataset generated", "path": dataset_path}
    except Exception as e:
        raise HTTPException(500, f"Dataset generation failed: {str(e)}")

@app.post("/train-model")
async def train_model(request: dict):
    return {"message": "Training would start here", "path": "models/demo.pt"}

@app.post("/test-model")
async def test_model(request: dict):
    return {"results": {"total_detections": 1, "annotated_image": "demo_result.jpg"}}

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FIBO-Sim2Real Factory Server...")
    print("📱 Web UI: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
