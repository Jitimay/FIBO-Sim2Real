#!/usr/bin/env python3
"""
Test real FIBO API connection
"""
import os
import sys
from dotenv import load_dotenv
sys.path.append('backend')

from fibo_client import FIBOClient

def test_fibo():
    load_dotenv()
    
    api_key = os.getenv("FIBO_API_KEY")
    if not api_key:
        print("❌ FIBO_API_KEY not found in .env file")
        return False
    
    print(f"🔑 API Key found: {api_key[:10]}...")
    
    try:
        client = FIBOClient()
        print("✅ FIBO client initialized")
        
        # Test with a sample image (you'll need to provide one)
        test_image = "test_image.jpg"
        if not os.path.exists(test_image):
            print(f"⚠️  Test image not found: {test_image}")
            print("Create a test image to verify FIBO connection")
            return True
        
        params = {
            "seed": 12345,
            "background": "neutral",
            "light_intensity": 1.0
        }
        
        print("🚀 Testing FIBO image generation...")
        result = client.generate_image(test_image, params)
        
        print(f"✅ FIBO API working! Generated {len(result)} bytes")
        
        # Save test result
        with open("fibo_test_result.jpg", "wb") as f:
            f.write(result)
        print("💾 Test result saved as fibo_test_result.jpg")
        
        return True
        
    except Exception as e:
        print(f"❌ FIBO API error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_fibo()
    sys.exit(0 if success else 1)
