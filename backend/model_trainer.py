import os
from pathlib import Path
import torch
import cv2
import numpy as np
from PIL import Image

class ModelTrainer:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"🔧 ModelTrainer initialized with device: {self.device}")
        
    async def train_yolo(self, dataset_path: str) -> str:
        """Train YOLOv8 model on synthetic dataset"""
        
        try:
            from ultralytics import YOLO
        except ImportError:
            raise Exception("ultralytics package not installed. Please run: pip install ultralytics")
        
        # Check if dataset exists
        data_yaml_path = Path(dataset_path) / "data.yaml"
        if not data_yaml_path.exists():
            raise Exception(f"Dataset configuration not found: {data_yaml_path}")
        
        print(f"🤖 Starting YOLO training with dataset: {dataset_path}")
        print(f"📊 Using device: {self.device}")
        
        try:
            # Initialize YOLOv8 nano model
            print("📥 Loading YOLOv8 nano model...")
            model = YOLO('yolov8n.pt')
            
            # Create models directory
            models_dir = Path("models")
            models_dir.mkdir(exist_ok=True)
            
            # Training configuration
            print("🚀 Starting training...")
            results = model.train(
                data=str(data_yaml_path),
                epochs=10,  # Reduced for faster demo
                imgsz=640,
                batch=8,   # Reduced batch size
                device=self.device,
                project="models",
                name="fibo_synthetic",
                save=True,
                verbose=True,
                patience=5  # Early stopping
            )
            
            # Return path to trained weights
            model_path = "models/fibo_synthetic/weights/best.pt"
            
            # Check if model was actually created
            if not Path(model_path).exists():
                # Try alternative paths
                alt_paths = [
                    "models/fibo_synthetic/weights/last.pt",
                    "models/fibo_synthetic1/weights/best.pt",
                    "models/fibo_synthetic1/weights/last.pt"
                ]
                
                for alt_path in alt_paths:
                    if Path(alt_path).exists():
                        model_path = alt_path
                        break
                else:
                    raise Exception("Training completed but model weights not found")
            
            print(f"✅ Training completed successfully: {model_path}")
            return model_path
            
        except Exception as e:
            print(f"❌ Training failed: {str(e)}")
            raise Exception(f"YOLO training failed: {str(e)}")
    
    async def test_on_real_image(self, model_path: str, test_image_path: str) -> dict:
        """Test trained model on real image"""
        
        try:
            from ultralytics import YOLO
        except ImportError:
            raise Exception("ultralytics package not installed. Please run: pip install ultralytics")
        
        # Check if model exists
        if not Path(model_path).exists():
            raise Exception(f"Model not found: {model_path}")
        
        # Check if test image exists
        if not Path(test_image_path).exists():
            raise Exception(f"Test image not found: {test_image_path}")
        
        print(f"🧪 Testing model: {model_path} on image: {test_image_path}")
        
        try:
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
            results_dir = Path("results")
            results_dir.mkdir(exist_ok=True)
            annotated_path = results_dir / "annotated_result.jpg"
            
            annotated_img = results[0].plot()
            cv2.imwrite(str(annotated_path), annotated_img)
            
            print(f"✅ Testing completed: {len(detections)} detections found")
            
            return {
                "detections": detections,
                "annotated_image": str(annotated_path),
                "total_detections": len(detections)
            }
            
        except Exception as e:
            print(f"❌ Testing failed: {str(e)}")
            raise Exception(f"Model testing failed: {str(e)}")
    
    def export_to_onnx(self, model_path: str) -> str:
        """Export trained model to ONNX for edge deployment"""
        
        try:
            from ultralytics import YOLO
        except ImportError:
            raise Exception("ultralytics package not installed. Please run: pip install ultralytics")
        
        # Check if model exists
        if not Path(model_path).exists():
            raise Exception(f"Model not found: {model_path}")
        
        print(f"📦 Exporting model to ONNX: {model_path}")
        
        try:
            model = YOLO(model_path)
            
            # Export to ONNX
            onnx_path = model_path.replace('.pt', '.onnx')
            model.export(format='onnx', imgsz=640)
            
            # Check if ONNX file was created
            if not Path(onnx_path).exists():
                raise Exception("ONNX export completed but file not found")
            
            print(f"✅ Model exported successfully: {onnx_path}")
            return onnx_path
            
        except Exception as e:
            print(f"❌ Export failed: {str(e)}")
            raise Exception(f"ONNX export failed: {str(e)}")
