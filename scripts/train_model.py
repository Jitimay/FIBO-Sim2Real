#!/usr/bin/env python3
"""
Standalone script to train YOLOv8 model on synthetic dataset
"""
import argparse
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from model_trainer import ModelTrainer

async def main():
    parser = argparse.ArgumentParser(description='Train YOLOv8 model on synthetic dataset')
    parser.add_argument('--dataset', default='dataset', help='Path to dataset directory')
    parser.add_argument('--epochs', type=int, default=50, help='Number of training epochs')
    parser.add_argument('--batch_size', type=int, default=16, help='Batch size')
    
    args = parser.parse_args()
    
    dataset_yaml = os.path.join(args.dataset, 'data.yaml')
    if not os.path.exists(dataset_yaml):
        print(f"Error: Dataset not found: {dataset_yaml}")
        print("Run generate_dataset.py first to create a dataset")
        return 1
    
    print(f"🚀 Training YOLOv8 model...")
    print(f"📁 Dataset: {args.dataset}")
    print(f"🔄 Epochs: {args.epochs}")
    print(f"📦 Batch size: {args.batch_size}")
    
    try:
        trainer = ModelTrainer()
        
        # Train model
        model_path = await trainer.train_yolo(args.dataset)
        
        print(f"✅ Model trained successfully!")
        print(f"💾 Model saved to: {model_path}")
        print(f"🎯 Ready for testing on real images")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error training model: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
