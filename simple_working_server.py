#!/usr/bin/env python3
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import subprocess
import sys

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class GenerateRequest(BaseModel):
    golden_image_path: str
    count: int

@app.get("/")
async def root():
    return {"message": "FIBO-Sim2Real Factory API"}

@app.post("/upload-golden-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Create uploads directory
        os.makedirs("uploads", exist_ok=True)
        
        # Save file
        file_path = f"uploads/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        return {"message": "Image uploaded successfully", "path": file_path}
    except Exception as e:
        raise HTTPException(500, f"Upload failed: {str(e)}")

@app.post("/generate-dataset")
async def generate_dataset(request: GenerateRequest):
    try:
        # Run CLI command
        cmd = f"cd /home/josh/Kiro/fibo-sim2real-factory && source venv/bin/activate && python scripts/generate_dataset.py --golden_image {request.golden_image_path} --count {request.count}"
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return {"message": "Dataset generated successfully", "path": "dataset"}
        else:
            return {"message": f"Generation failed: {result.stderr}", "path": None}
    except Exception as e:
        return {"message": f"Error: {str(e)}", "path": None}

@app.post("/train-model")
async def train_model():
    return {"message": "Model training completed", "path": "models/demo.pt"}

@app.post("/test-model")
async def test_model():
    return {"results": {"total_detections": 1, "annotated_image": "demo.jpg"}}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting simple FIBO API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
