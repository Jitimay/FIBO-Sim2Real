#!/usr/bin/env python3
"""
Standalone script to generate synthetic dataset using FIBO
"""
import argparse
import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fibo_client import FIBOClient
from dataset_generator import DatasetGenerator

async def main():
    parser = argparse.ArgumentParser(description='Generate synthetic dataset using FIBO')
    parser.add_argument('--golden_image', required=True, help='Path to golden image')
    parser.add_argument('--count', type=int, default=1000, help='Number of images to generate')
    parser.add_argument('--output', default='dataset', help='Output dataset directory')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.golden_image):
        print(f"Error: Golden image not found: {args.golden_image}")
        return 1
    
    print(f"🚀 Generating {args.count} synthetic images using FIBO...")
    print(f"📁 Golden image: {args.golden_image}")
    print(f"📁 Output directory: {args.output}")
    
    try:
        # Initialize FIBO client and dataset generator
        fibo_client = FIBOClient()
        dataset_gen = DatasetGenerator(fibo_client)
        
        # Generate dataset
        dataset_path = await dataset_gen.generate_synthetic_dataset(
            args.golden_image, args.count
        )
        
        print(f"✅ Dataset generated successfully!")
        print(f"📁 Dataset path: {dataset_path}")
        print(f"📊 Training images: {int(args.count * 0.8)}")
        print(f"📊 Validation images: {int(args.count * 0.2)}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error generating dataset: {str(e)}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
