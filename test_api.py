#!/usr/bin/env python3
"""
Test script for FIBO-Sim2Real Factory API
"""
import requests
import json
import time

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
    except Exception as e:
        print(f"Health check failed: {e}")
    return False

def test_train_model():
    """Test train model endpoint"""
    try:
        payload = {"dataset_path": "dataset"}
        response = requests.post(
            f"{API_BASE}/train-model",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        print(f"Train model: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Train model test failed: {e}")
    return False

def main():
    print("🧪 Testing FIBO-Sim2Real Factory API...")
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(2)
    
    # Test health endpoint
    if not test_health():
        print("❌ Health check failed - server may not be running")
        return 1
    
    print("✅ Health check passed")
    
    # Test train model endpoint
    print("🧪 Testing train model endpoint...")
    if test_train_model():
        print("✅ Train model endpoint working")
    else:
        print("❌ Train model endpoint failed")
    
    print("🎉 API tests completed!")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())