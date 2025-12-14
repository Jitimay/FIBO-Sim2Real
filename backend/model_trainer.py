import os
from pathlib import Path
from ultralytics import YOLO
import torch
import cv2
import numpy as np
from PIL import Image

class ModelTrainer:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    async def train_yolo(self, dataset_path: str) -> str:
        """Train YOLOv8 model on synthetic dataset"""
        
        # Initialize YOLOv8 nano model
        model = YOLO('yolov8n.pt')
        
        # Training configuration
        results = model.train(
            data=f"{dataset_path}/data.yaml",
            epochs=50,
            imgsz=640,
            batch=16,
            device=self.device,
            project="models",
            name="fibo_synthetic",
            save=True,
            verbose=True
        )
        
        # Return path to trained weights
        model_path = "models/fibo_synthetic/weights/best.pt"
        return model_path
    
    async def test_on_real_image(self, model_path: str, test_image_path: str) -> dict:
        """Test trained model on real image"""
        
        # Load trained model
        model = YOLO(model_path)
        
        # Run inference
        results = model(test_image_path)
        
        # Extract results
        detections = []
        for r in results:
            boxes = r.boxes
            if boxes is not None:
                for box in boxes:
                    detections.append({
                        "bbox": box.xyxy[0].tolist(),
                        "confidence": float(box.conf[0]),
                        "class": int(box.cls[0])
                    })
        
        # Save annotated image
        annotated_path = "results/annotated_result.jpg"
        os.makedirs("results", exist_ok=True)
        
        annotated_img = results[0].plot()
        cv2.imwrite(annotated_path, annotated_img)
        
        return {
            "detections": detections,
            "annotated_image": annotated_path,
            "total_detections": len(detections)
        }
    
    def export_to_onnx(self, model_path: str) -> str:
        """Export trained model to ONNX for edge deployment"""
        
        model = YOLO(model_path)
        
        # Export to ONNX
        onnx_path = model_path.replace('.pt', '.onnx')
        model.export(format='onnx', imgsz=640)
        
        return onnx_path
