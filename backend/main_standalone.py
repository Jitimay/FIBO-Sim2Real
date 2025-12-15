from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import sys
import json
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from fibo_client import FIBOClient
from dataset_generator import DatasetGenerator
from model_trainer import ModelTrainer

app = FastAPI(title="FIBO-Sim2Real Factory")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request bodies
class GenerateDatasetRequest(BaseModel):
    golden_image_path: str
    count: int = 1000

class TrainModelRequest(BaseModel):
    dataset_path: str

class TestModelRequest(BaseModel):
    model_path: str
    test_image_path: str

class ExportModelRequest(BaseModel):
    model_path: str

# Initialize services
print("🔧 Initializing FIBO client...")
fibo_client = FIBOClient()
print("🔧 Initializing dataset generator...")
dataset_gen = DatasetGenerator(fibo_client)
print("🔧 Initializing model trainer...")
trainer = ModelTrainer()
print("✅ All services initialized successfully!")

@app.get("/")
async def root():
    return {"message": "FIBO-Sim2Real Factory API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["fibo_client", "dataset_generator", "model_trainer"]}

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
    
    return {"message": "Image uploaded successfully", "path": str(file_path)}

@app.post("/generate-dataset")
async def generate_dataset(request: GenerateDatasetRequest):
    try:
        print(f"🎨 Generating dataset: {request.count} images from {request.golden_image_path}")
        dataset_path = await dataset_gen.generate_synthetic_dataset(
            request.golden_image_path, request.count
        )
        print(f"✅ Dataset generated successfully: {dataset_path}")
        return {"message": "Dataset generated successfully", "path": dataset_path}
    except Exception as e:
        print(f"❌ Dataset generation failed: {str(e)}")
        raise HTTPException(500, f"Dataset generation failed: {str(e)}")

@app.post("/train-model")
async def train_model(request: TrainModelRequest):
    try:
        print(f"🤖 Training model on dataset: {request.dataset_path}")
        model_path = await trainer.train_yolo(request.dataset_path)
        print(f"✅ Model trained successfully: {model_path}")
        return {"message": "Model trained successfully", "path": model_path}
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        raise HTTPException(500, f"Training failed: {str(e)}")

@app.post("/test-model")
async def test_model(request: TestModelRequest):
    try:
        print(f"🧪 Testing model: {request.model_path} on {request.test_image_path}")
        results = await trainer.test_on_real_image(request.model_path, request.test_image_path)
        print(f"✅ Testing completed: {results['total_detections']} detections")
        return {"results": results}
    except Exception as e:
        print(f"❌ Testing failed: {str(e)}")
        raise HTTPException(500, f"Testing failed: {str(e)}")

@app.post("/export-model")
async def export_model(request: ExportModelRequest):
    try:
        print(f"📦 Exporting model: {request.model_path}")
        onnx_path = trainer.export_to_onnx(request.model_path)
        print(f"✅ Model exported successfully: {onnx_path}")
        return {"message": "Model exported successfully", "onnx_path": onnx_path}
    except Exception as e:
        print(f"❌ Export failed: {str(e)}")
        raise HTTPException(500, f"Export failed: {str(e)}")

# Serve static files (frontend)
try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
    print("✅ Frontend static files mounted successfully")
except Exception as e:
    print(f"⚠️ Could not mount frontend static files: {e}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FIBO-Sim2Real Factory Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🌐 Web UI will be available at: http://localhost:8000")
    print("📋 API docs available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)