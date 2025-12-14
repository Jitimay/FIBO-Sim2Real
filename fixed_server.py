#!/usr/bin/env python3
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os, asyncio
sys.path.append('backend')

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
        print(f"🚀 Generating {request.count} images from {request.golden_image_path}")
        
        # Import here to avoid startup issues
        from fibo_client import FIBOClient
        from dataset_generator import DatasetGenerator
        
        client = FIBOClient()
        gen = DatasetGenerator(client)
        
        # Run the async function
        path = await gen.generate_synthetic_dataset(request.golden_image_path, request.count)
        
        return {"message": "Dataset generated successfully", "path": path}
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(500, f"Generation failed: {str(e)}")

@app.post("/train-model")
async def train_model():
    return {"message": "Model training started", "path": "models/demo.pt"}

@app.post("/test-model") 
async def test_model():
    return {"results": {"total_detections": 1, "annotated_image": "demo.jpg"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
