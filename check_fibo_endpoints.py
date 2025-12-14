#!/usr/bin/env python3
"""
Check available FIBO API endpoints
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("FIBO_API_KEY")
base_urls = [
    "https://engine.prod.bria-api.com",
    "https://api.bria.ai",
    "https://bria-api.com"
]

endpoints_to_try = [
    "/v1/text-to-image",
    "/v1/generate", 
    "/v1/fibo",
    "/text-to-image",
    "/generate",
    "/fibo"
]

headers_to_try = [
    {"api_token": api_key},
    {"Authorization": f"Bearer {api_key}"},
    {"X-API-Key": api_key}
]

print(f"Testing FIBO API endpoints with key: {api_key[:10]}...")

for base_url in base_urls:
    print(f"\n🔍 Testing base URL: {base_url}")
    
    for endpoint in endpoints_to_try:
        for headers in headers_to_try:
            url = f"{base_url}{endpoint}"
            
            try:
                # Try GET first to see if endpoint exists
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code != 404:
                    print(f"  ✅ {url} - Status: {response.status_code}")
                    if response.status_code == 200:
                        print(f"     Response: {response.text[:100]}...")
                    elif response.status_code == 405:
                        print(f"     Method not allowed - endpoint exists!")
                
            except Exception as e:
                continue

print("\n🔍 Trying POST requests on promising endpoints...")

# Test specific endpoints that might work
test_endpoints = [
    "https://engine.prod.bria-api.com/v1/text-to-image",
    "https://api.bria.ai/v1/generate"
]

for url in test_endpoints:
    for headers in headers_to_try:
        try:
            response = requests.post(
                url, 
                headers=headers,
                json={"prompt": "test"},
                timeout=10
            )
            
            print(f"POST {url}: {response.status_code}")
            if response.status_code not in [404, 401]:
                print(f"  Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"POST {url}: Error - {e}")
