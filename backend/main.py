from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json
from pathlib import Path
from .fibo_client import FIBOClient
from .dataset_generator import DatasetGenerator
from .model_trainer import ModelTrainer

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
trainer = ModelTrainer()

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
async def generate_dataset(golden_image_path: str, count: int = 1000):
    try:
        dataset_path = await dataset_gen.generate_synthetic_dataset(
            golden_image_path, count
        )
        return {"message": "Dataset generated", "path": dataset_path}
    except Exception as e:
        raise HTTPException(500, f"Dataset generation failed: {str(e)}")

@app.post("/train-model")
async def train_model(dataset_path: str):
    try:
        model_path = await trainer.train_yolo(dataset_path)
        return {"message": "Model trained", "path": model_path}
    except Exception as e:
        raise HTTPException(500, f"Training failed: {str(e)}")

@app.post("/test-model")
async def test_model(model_path: str, test_image_path: str):
    try:
        results = await trainer.test_on_real_image(model_path, test_image_path)
        return {"results": results}
    except Exception as e:
        raise HTTPException(500, f"Testing failed: {str(e)}")

@app.post("/export-model")
async def export_model(model_path: str):
    try:
        onnx_path = trainer.export_to_onnx(model_path)
        return {"message": "Model exported", "onnx_path": onnx_path}
    except Exception as e:
        raise HTTPException(500, f"Export failed: {str(e)}")

# Serve static files
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
