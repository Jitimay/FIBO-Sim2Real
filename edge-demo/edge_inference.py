#!/usr/bin/env python3
"""
Edge inference script for Raspberry Pi / Jetson Nano
Supports both ONNX and PyTorch models
"""
import argparse
import cv2
import numpy as np
import time
import os

try:
    import onnxruntime as ort
    ONNX_AVAILABLE = True
except ImportError:
    ONNX_AVAILABLE = False
    print("Warning: ONNX Runtime not available. Install with: pip install onnxruntime")

try:
    from ultralytics import YOLO
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("Warning: Ultralytics not available. Install with: pip install ultralytics")

class EdgeInference:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model_type = self._detect_model_type()
        self.model = self._load_model()
        
    def _detect_model_type(self) -> str:
        if self.model_path.endswith('.onnx'):
            return 'onnx'
        elif self.model_path.endswith('.pt'):
            return 'torch'
        else:
            raise ValueError("Unsupported model format. Use .onnx or .pt")
    
    def _load_model(self):
        if self.model_type == 'onnx':
            if not ONNX_AVAILABLE:
                raise RuntimeError("ONNX Runtime not available")
            return ort.InferenceSession(self.model_path)
        elif self.model_type == 'torch':
            if not TORCH_AVAILABLE:
                raise RuntimeError("Ultralytics not available")
            return YOLO(self.model_path)
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for inference"""
        # Resize to 640x640
        resized = cv2.resize(image, (640, 640))
        
        if self.model_type == 'onnx':
            # Convert BGR to RGB and normalize
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            normalized = rgb.astype(np.float32) / 255.0
            # Add batch dimension and transpose to NCHW
            return np.transpose(normalized[None, :, :, :], (0, 3, 1, 2))
        else:
            return resized
    
    def inference(self, image: np.ndarray) -> list:
        """Run inference on preprocessed image"""
        if self.model_type == 'onnx':
            input_name = self.model.get_inputs()[0].name
            outputs = self.model.run(None, {input_name: image})
            return self._postprocess_onnx(outputs[0])
        else:
            results = self.model(image, verbose=False)
            return self._postprocess_torch(results[0])
    
    def _postprocess_onnx(self, output: np.ndarray) -> list:
        """Postprocess ONNX model output"""
        detections = []
        # Simple postprocessing - adapt based on your model output format
        for detection in output[0]:  # Assuming batch size 1
            if detection[4] > 0.5:  # Confidence threshold
                detections.append({
                    'bbox': detection[:4].tolist(),
                    'confidence': float(detection[4]),
                    'class': int(detection[5]) if len(detection) > 5 else 0
                })
        return detections
    
    def _postprocess_torch(self, result) -> list:
        """Postprocess PyTorch model output"""
        detections = []
        if result.boxes is not None:
            for box in result.boxes:
                detections.append({
                    'bbox': box.xyxy[0].tolist(),
                    'confidence': float(box.conf[0]),
                    'class': int(box.cls[0])
                })
        return detections
    
    def draw_detections(self, image: np.ndarray, detections: list) -> np.ndarray:
        """Draw bounding boxes on image"""
        for det in detections:
            bbox = det['bbox']
            conf = det['confidence']
            
            # Draw bounding box
            cv2.rectangle(image, 
                         (int(bbox[0]), int(bbox[1])), 
                         (int(bbox[2]), int(bbox[3])), 
                         (0, 255, 0), 2)
            
            # Draw confidence
            label = f"Object: {conf:.2f}"
            cv2.putText(image, label, 
                       (int(bbox[0]), int(bbox[1]) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return image

def main():
    parser = argparse.ArgumentParser(description='Edge inference for FIBO-trained models')
    parser.add_argument('--model', required=True, help='Path to model (.pt or .onnx)')
    parser.add_argument('--source', default='0', help='Video source (0 for webcam, or image path)')
    parser.add_argument('--output', help='Output video path (optional)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"Error: Model not found: {args.model}")
        return 1
    
    print(f"🚀 Starting edge inference...")
    print(f"🤖 Model: {args.model}")
    print(f"📹 Source: {args.source}")
    
    try:
        # Initialize inference engine
        inference_engine = EdgeInference(args.model)
        
        # Check if source is webcam or image
        if args.source.isdigit():
            # Webcam mode
            cap = cv2.VideoCapture(int(args.source))
            
            if not cap.isOpened():
                print("Error: Could not open webcam")
                return 1
            
            print("📹 Press 'q' to quit")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                start_time = time.time()
                
                # Preprocess
                processed = inference_engine.preprocess_image(frame)
                
                # Inference
                detections = inference_engine.inference(processed)
                
                # Draw results
                result_frame = inference_engine.draw_detections(frame, detections)
                
                # Calculate FPS
                fps = 1.0 / (time.time() - start_time)
                cv2.putText(result_frame, f"FPS: {fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Show frame
                cv2.imshow('FIBO Edge Inference', result_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
        else:
            # Image mode
            if not os.path.exists(args.source):
                print(f"Error: Image not found: {args.source}")
                return 1
            
            image = cv2.imread(args.source)
            
            # Preprocess and inference
            processed = inference_engine.preprocess_image(image)
            detections = inference_engine.inference(processed)
            
            # Draw results
            result_image = inference_engine.draw_detections(image, detections)
            
            print(f"✅ Found {len(detections)} detections")
            
            # Save or show result
            if args.output:
                cv2.imwrite(args.output, result_image)
                print(f"💾 Result saved to: {args.output}")
            else:
                cv2.imshow('Result', result_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during inference: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
