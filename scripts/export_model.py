#!/usr/bin/env python3
"""
Export trained model to ONNX for edge deployment
"""
import argparse
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from model_trainer import ModelTrainer

def main():
    parser = argparse.ArgumentParser(description='Export model to ONNX')
    parser.add_argument('--model', default='models/fibo_synthetic/weights/best.pt', 
                       help='Path to trained model')
    parser.add_argument('--output', help='Output ONNX path (optional)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"Error: Model not found: {args.model}")
        return 1
    
    print(f"📦 Exporting model to ONNX...")
    print(f"🤖 Input model: {args.model}")
    
    try:
        trainer = ModelTrainer()
        onnx_path = trainer.export_to_onnx(args.model)
        
        if args.output:
            os.rename(onnx_path, args.output)
            onnx_path = args.output
        
        print(f"✅ Model exported successfully!")
        print(f"💾 ONNX model: {onnx_path}")
        print(f"🚀 Ready for edge deployment")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error exporting model: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
