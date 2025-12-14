#!/usr/bin/env python3
"""
Test trained model on real images
"""
import argparse
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from model_trainer import ModelTrainer

async def main():
    parser = argparse.ArgumentParser(description='Test trained model on real image')
    parser.add_argument('--model', default='models/fibo_synthetic/weights/best.pt', help='Path to trained model')
    parser.add_argument('--image', required=True, help='Path to test image')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.model):
        print(f"Error: Model not found: {args.model}")
        print("Run train_model.py first to train a model")
        return 1
        
    if not os.path.exists(args.image):
        print(f"Error: Test image not found: {args.image}")
        return 1
    
    print(f"🔍 Testing model on real image...")
    print(f"🤖 Model: {args.model}")
    print(f"🖼️  Test image: {args.image}")
    
    try:
        trainer = ModelTrainer()
        
        # Test on real image
        results = await trainer.test_on_real_image(args.model, args.image)
        
        print(f"✅ Testing complete!")
        print(f"🎯 Detections found: {results['total_detections']}")
        print(f"📊 Annotated result saved to: {results['annotated_image']}")
        
        for i, detection in enumerate(results['detections']):
            print(f"   Detection {i+1}: confidence={detection['confidence']:.3f}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error testing model: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
