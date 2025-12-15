#!/usr/bin/env python3
"""
Test the training endpoint directly
"""
import requests
import json

def test_training_endpoint():
    print("🧪 Testing training endpoint...")
    
    # Test data
    payload = {
        "dataset_path": "dataset"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/train-model",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=30
        )
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📋 Response headers: {dict(response.headers)}")
        print(f"📄 Response text: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Training successful: {result}")
            return True
        else:
            print(f"❌ Training failed with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is it running?")
        print("🚀 Start server with: python quick_fix_server.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_endpoints():
    print("🧪 Testing all endpoints...")
    
    endpoints = [
        ("GET", "/health", None),
        ("POST", "/train-model", {"dataset_path": "dataset"}),
        ("POST", "/test-model", {"model_path": "models/test.pt", "test_image_path": "test.jpg"}),
        ("POST", "/export-model", {"model_path": "models/test.pt"})
    ]
    
    for method, endpoint, data in endpoints:
        try:
            url = f"http://localhost:8000{endpoint}"
            
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(data) if data else None,
                    timeout=30
                )
            
            print(f"{method} {endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Success")
            else:
                print(f"  ❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"{method} {endpoint}: ❌ Error: {e}")

if __name__ == "__main__":
    print("🔧 FIBO-Sim2Real Factory - Endpoint Testing")
    print("=" * 50)
    
    # Test training specifically
    success = test_training_endpoint()
    
    print("\n" + "=" * 50)
    
    # Test all endpoints
    test_all_endpoints()
    
    if success:
        print("\n✅ Training endpoint is working!")
    else:
        print("\n❌ Training endpoint has issues")
        print("🔧 Try restarting the server: python quick_fix_server.py")