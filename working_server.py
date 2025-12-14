#!/usr/bin/env python3
import os
import sys
import asyncio
from pathlib import Path

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class GenerateRequest(BaseModel):
    golden_image_path: str
    count: int

@app.post("/upload-golden-image")
async def upload(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    path = f"uploads/{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())
    return {"message": "Uploaded", "path": path}

@app.post("/generate-dataset")
async def generate(request: GenerateRequest):
    try:
        print(f"🚀 Starting generation: {request.count} images from {request.golden_image_path}")
        
        # Import modules
        from fibo_client import FIBOClient
        from dataset_generator import DatasetGenerator
        
        # Initialize
        client = FIBOClient()
        gen = DatasetGenerator(client)
        
        # Generate dataset
        dataset_path = await gen.generate_synthetic_dataset(
            request.golden_image_path, 
            request.count
        )
        
        print(f"✅ Dataset generated: {dataset_path}")
        return {"message": "Dataset generated successfully", "path": dataset_path}
        
    except Exception as e:
        print(f"❌ Generation error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Generation failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FIBO API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
