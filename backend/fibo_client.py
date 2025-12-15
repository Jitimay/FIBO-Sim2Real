import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any
import base64
from PIL import Image, ImageEnhance, ImageFilter
import io
import random

import os
import requests
import time
from dotenv import load_dotenv
from typing import Dict, Any

# Load key from .env file
load_dotenv()

class FIBOClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BRIA_API_TOKEN")
        if not self.api_key:
            raise ValueError("BRIA_API_TOKEN not found in environment. Please set it in your .env file.")
        
        self.base_url = "https://api.bria.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        print("🔑 Bria API Client Initialized (v1, Async Flow)")

    def _submit_request(self, prompt: str, source_image_path: str = None) -> str:
        """Submits the image generation request and returns the status URL."""
        
        # Use the "Image-to-Image" endpoint if a source image is provided
        endpoint = "/image-to-image/base" if source_image_path else "/text-to-image/base"
        url = self.base_url + endpoint
        
        print(f"Submitting request to: {url}")
        
        # The payload is sent as multipart-form data, not JSON, when an image is present
        data = {"prompt": prompt}
        files = {}
        headers = {"Authorization": f"Bearer {self.api_key}"} # No Content-Type for multipart

        if source_image_path:
            files['image'] = (os.path.basename(source_image_path), open(source_image_path, 'rb'), 'image/jpeg')
        
        try:
            response = requests.post(url, data=data, files=files, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            status_url = response_data.get("status_url")
            
            if not status_url:
                raise ValueError("API did not return a status_url.")
                
            print(f"Request submitted successfully. Status URL: {status_url}")
            return status_url
            
        finally:
            if 'image' in files:
                files['image'][1].close()

    def _poll_for_results(self, status_url: str, max_attempts: int = 30) -> Dict[str, Any]:
        """Polls the status URL until the image is generated or an error occurs."""
        print(f"Polling status URL: {status_url}")
        
        # Use headers with Content-Type for GET requests
        poll_headers = {"Authorization": f"Bearer {self.api_key}"}

        for i in range(max_attempts):
            response = requests.get(status_url, headers=poll_headers)
            response.raise_for_status()
            
            status_data = response.json()
            status = status_data.get("status")
            
            if status == "COMPLETED":
                print(f"Status: COMPLETED (Attempt {i+1})")
                return status_data
            
            elif status == "ERROR":
                error_details = status_data.get("error", "Unknown error")
                raise Exception(f"Image generation failed: {error_details}")
                
            print(f"Status: {status} (Attempt {i+1}). Waiting...")
            time.sleep(3)
            
        raise TimeoutError("Image generation timed out after several attempts.")

    def _download_image(self, image_url: str) -> bytes:
        """Downloads the image from the given URL."""
        print(f"Downloading final image from: {image_url}")
        
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        
        return image_response.content

    def generate_image(self, prompt: str, source_image_path: str = None) -> Dict[str, Any]:
        """
        Runs the full asynchronous workflow to generate and retrieve an image.
        
        Returns a dictionary containing the image bytes and the final API response data.
        """
        # 1. Submit the generation request
        status_url = self._submit_request(prompt, source_image_path)
        
        # 2. Poll the status URL until complete
        completed_data = self._poll_for_results(status_url)
        
        # 3. Extract image URL from the final response
        image_url = completed_data.get("result", [{}])[0].get("image_url")
        if not image_url:
            raise ValueError("Completed job did not contain an image URL.")

        # 4. Download the final image
        image_bytes = self._download_image(image_url)
        
        print("✅ Image successfully generated and downloaded.")
        
        return {
            "image_bytes": image_bytes,
            "api_response": completed_data # Return the full response for bounding box extraction
        }

    def get_bounding_box(self, api_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts bounding box information from the final Bria API response.
        """
        try:
            # The bounding box is in the 'result' list of the completed data
            result_data = api_response.get("result", [{}])[0]
            chains = result_data.get("chains", [])
            
            if not chains:
                print("⚠️ No 'chains' data found for bounding box. Returning a default box.")
                return {"bbox": [0.0, 0.0, 1.0, 1.0], "confidence": 0.5, "class": "object"}

            # Find the object from the source image
            source_object = next((obj for obj in chains if obj.get("source") == "source_image"), None)
            
            if not source_object or "bounding_box" not in source_object:
                print("⚠️ No source object bounding box found. Returning a default box.")
                return {"bbox": [0.0, 0.0, 1.0, 1.0], "confidence": 0.5, "class": "object"}

            # Bria returns [x_min, y_min, width, height]
            x1, y1, w, h = source_object["bounding_box"]
            x2 = x1 + w
            y2 = y1 + h

            bbox = [x1, y1, x2, y2]
            print(f"✅ Extracted bounding box: {bbox}")

            return {
                "bbox": bbox,
                "confidence": source_object.get("confidence", 0.9),
                "class": source_object.get("label", "object")
            }
            
        except (KeyError, IndexError, TypeError) as e:
            print(f"❌ Error parsing bounding box from API response: {e}")
            raise ValueError("Could not extract bounding box from the provided API response.")

