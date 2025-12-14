#!/usr/bin/env python3
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

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
    # Simple test - just run the CLI command
    import subprocess
    import sys
    
    try:
        print(f"🚀 Generating {request.count} images...")
        
        # Run the CLI script
        result = subprocess.run([
            sys.executable, "scripts/generate_dataset.py",
            "--golden_image", request.golden_image_path,
            "--count", str(request.count)
        ], capture_output=True, text=True, cwd="/home/josh/Kiro/fibo-sim2real-factory")
        
        if result.returncode == 0:
            return {"message": "Dataset generated successfully", "path": "dataset"}
        else:
            print(f"Error: {result.stderr}")
            return {"message": f"Generation failed: {result.stderr}", "path": None}
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"message": f"Error: {str(e)}", "path": None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
