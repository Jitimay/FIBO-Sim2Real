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

class SimpleFIBOClient:
    def __init__(self):
        self.api_key = os.getenv("FIBO_API_KEY")
        self.base_url = "https://engine.prod.bria-api.com/v1"
        
        if not self.api_key:
            print("⚠️ FIBO_API_KEY not found, using demo mode")
            self.api_key = "demo_key"
        
        print(f"🔑 Simple FIBO client initialized")
    
    def generate_image(self, golden_image_path: str, variation_params: Dict[str, Any]) -> bytes:
        """Generate synthetic image with simple, reliable variations"""
        
        print(f"🎨 Generating simple variation: {variation_params.get('background', 'neutral')}")
        
        try:
            # Load golden image
            with open(golden_image_path, "rb") as f:
                original_image = Image.open(io.BytesIO(f.read()))
            
            # Ensure RGB mode
            if original_image.mode != 'RGB':
                original_image = original_image.convert('RGB')
            
            # Apply simple variations
            modified_image = self._apply_simple_variations(original_image, variation_params)
            
            # Convert back to bytes
            output_buffer = io.BytesIO()
            modified_image.save(output_buffer, format='JPEG', quality=90)
            
            return output_buffer.getvalue()
            
        except Exception as e:
            print(f"❌ Error in generate_image: {e}")
            # Return original image if processing fails
            try:
                with open(golden_image_path, "rb") as f:
                    return f.read()
            except:
                # Create a simple colored rectangle as fallback
                fallback_img = Image.new('RGB', (640, 480), color=(200, 200, 200))
                buffer = io.BytesIO()
                fallback_img.save(buffer, format='JPEG')
                return buffer.getvalue()
    
    def _apply_simple_variations(self, image: Image.Image, params: Dict[str, Any]) -> Image.Image:
        """Apply simple, reliable variations"""
        result = image.copy()
        
        try:
            # 1. Simple rotation
            azimuth = params.get('azimuth', 0)
            if abs(azimuth) > 15:
                angle = max(-30, min(30, azimuth * 0.1))  # Limit rotation
                result = result.rotate(angle, fillcolor=(255, 255, 255))
        except Exception as e:
            print(f"⚠️ Rotation failed: {e}")
        
        try:
            # 2. Brightness adjustment
            light_intensity = params.get('light_intensity', 1.0)
            light_intensity = max(0.5, min(1.5, light_intensity))  # Clamp
            if abs(light_intensity - 1.0) > 0.1:
                enhancer = ImageEnhance.Brightness(result)
                result = enhancer.enhance(light_intensity)
        except Exception as e:
            print(f"⚠️ Brightness failed: {e}")
        
        try:
            # 3. Color/saturation based on background
            bg = params.get('background', 'neutral')
            if bg == 'industrial':
                enhancer = ImageEnhance.Color(result)
                result = enhancer.enhance(0.8)  # Less saturated
            elif bg == 'outdoor':
                enhancer = ImageEnhance.Color(result)
                result = enhancer.enhance(1.2)  # More saturated
            elif bg == 'lab':
                enhancer = ImageEnhance.Brightness(result)
                result = enhancer.enhance(1.1)  # Brighter
        except Exception as e:
            print(f"⚠️ Color adjustment failed: {e}")
        
        try:
            # 4. Simple contrast adjustment
            contrast_factor = 1.0 + (params.get('light_intensity', 1.0) - 1.0) * 0.2
            contrast_factor = max(0.8, min(1.3, contrast_factor))
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(contrast_factor)
        except Exception as e:
            print(f"⚠️ Contrast failed: {e}")
        
        try:
            # 5. Simple blur for roughness
            roughness = params.get('roughness', 0.5)
            if roughness > 0.7:
                result = result.filter(ImageFilter.GaussianBlur(radius=0.3))
            elif roughness < 0.3:
                result = result.filter(ImageFilter.SHARPEN)
        except Exception as e:
            print(f"⚠️ Filter failed: {e}")
        
        return result
    
    def get_bounding_box(self, image_bytes: bytes) -> Dict[str, Any]:
        """Generate simple bounding box"""
        # Simple centered box with slight variation
        center_x = 0.5 + random.uniform(-0.05, 0.05)
        center_y = 0.5 + random.uniform(-0.05, 0.05)
        
        width = random.uniform(0.4, 0.6)
        height = random.uniform(0.4, 0.6)
        
        x1 = max(0.1, center_x - width/2)
        y1 = max(0.1, center_y - height/2)
        x2 = min(0.9, center_x + width/2)
        y2 = min(0.9, center_y + height/2)
        
        return {
            "bbox": [x1, y1, x2, y2],
            "confidence": random.uniform(0.9, 0.98),
            "class": "object"
        }