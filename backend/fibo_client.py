import requests
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any
import base64
from PIL import Image, ImageEnhance, ImageFilter
import io
import random

load_dotenv()

class FIBOClient:
    def __init__(self):
        self.api_key = os.getenv("FIBO_API_KEY")
        # Note: Actual FIBO endpoint needs to be confirmed with Bria documentation
        self.base_url = "https://engine.prod.bria-api.com/v1"
        
        if not self.api_key:
            raise ValueError("FIBO_API_KEY not found in environment")
        
        print(f"🔑 FIBO API Key configured: {self.api_key[:10]}...")
    
    def generate_image(self, golden_image_path: str, variation_params: Dict[str, Any]) -> bytes:
        """Generate synthetic image using FIBO-style variations"""
        
        # For hackathon demo: Create realistic variations of the golden image
        # In production: Replace with actual FIBO API call
        
        print(f"🎨 Generating FIBO-style variation with params: {variation_params}")
        
        # Load golden image
        with open(golden_image_path, "rb") as f:
            original_image = Image.open(io.BytesIO(f.read()))
        
        # Apply FIBO-style transformations based on parameters
        modified_image = self._apply_fibo_variations(original_image, variation_params)
        
        # Convert back to bytes
        output_buffer = io.BytesIO()
        modified_image.save(output_buffer, format='JPEG', quality=90)
        
        # TODO: Replace with actual FIBO API call:
        # response = requests.post(
        #     f"{self.base_url}/correct-endpoint",
        #     headers={"api_token": self.api_key},
        #     files={"file": f.read()},
        #     data={"prompt": self._build_prompt(variation_params)}
        # )
        
        return output_buffer.getvalue()
    
    def _apply_fibo_variations(self, image: Image.Image, params: Dict[str, Any]) -> Image.Image:
        """Apply FIBO-style variations to demonstrate the concept"""
        
        # Start with original
        result = image.copy()
        
        # Apply lighting variations
        light_intensity = params.get('light_intensity', 1.0)
        if light_intensity != 1.0:
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance(light_intensity)
        
        # Apply background changes (simulate different backgrounds)
        bg = params.get('background', 'neutral')
        if bg != 'neutral':
            # Simulate background change by adjusting color tone
            if bg == 'industrial':
                enhancer = ImageEnhance.Color(result)
                result = enhancer.enhance(0.8)  # More muted colors
            elif bg == 'outdoor':
                enhancer = ImageEnhance.Color(result)
                result = enhancer.enhance(1.2)  # More vibrant
        
        # Apply material property changes
        roughness = params.get('roughness', 0.5)
        if roughness > 0.7:
            # Add slight blur for rough surfaces
            result = result.filter(ImageFilter.GaussianBlur(radius=0.5))
        elif roughness < 0.3:
            # Enhance sharpness for smooth surfaces
            result = result.filter(ImageFilter.UnsharpMask())
        
        # Add slight rotation for camera angle simulation
        elevation = params.get('elevation', 0)
        if abs(elevation) > 15:
            angle = elevation * 0.1  # Small rotation
            result = result.rotate(angle, expand=False, fillcolor='white')
        
        # Add noise if specified
        noise_level = params.get('noise', 0.0)
        if noise_level > 0:
            # Add subtle noise
            import numpy as np
            img_array = np.array(result)
            noise = np.random.normal(0, noise_level * 25, img_array.shape)
            noisy_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)
            result = Image.fromarray(noisy_array)
        
        return result
    
    def _build_prompt(self, params: Dict[str, Any]) -> str:
        """Build FIBO prompt from variation parameters"""
        base_prompt = "high quality product photography"
        
        # Add lighting conditions
        lighting = params.get('light_intensity', 1.0)
        if lighting > 1.2:
            base_prompt += ", bright lighting"
        elif lighting < 0.8:
            base_prompt += ", soft lighting"
        
        # Add background
        bg = params.get('background', 'neutral')
        bg_map = {
            'industrial': ', industrial background, factory setting',
            'outdoor': ', outdoor natural background',
            'lab': ', clean laboratory background, white',
            'warehouse': ', warehouse background, shelves',
            'neutral': ', clean white background'
        }
        base_prompt += bg_map.get(bg, ', neutral background')
        
        return base_prompt
    
    def get_bounding_box(self, image_bytes: bytes) -> Dict[str, Any]:
        """Get bounding box - assumes centered object for synthetic images"""
        return {
            "bbox": [0.2, 0.2, 0.8, 0.8],  # x1, y1, x2, y2 normalized
            "confidence": 0.95,
            "class": "object"
        }
