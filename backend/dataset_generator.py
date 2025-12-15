import os
import json
import random
from pathlib import Path
from typing import List, Dict, Any
import numpy as np
from PIL import Image
import io
from tqdm import tqdm

class DatasetGenerator:
    def __init__(self, fibo_client):
        self.fibo_client = fibo_client
        
    def generate_prompt(self) -> str:
        """Generates a descriptive text prompt for the Bria API."""
        
        base_object = "a photo of the user-provided object"

        environments = [
            "in a clean, modern laboratory setting",
            "on a workbench in a cluttered garage",
            "in a bright, sterile factory environment",
            "on a wooden table in an office",
            "outdoors on a patch of green grass",
            "on a metal shelf in a warehouse",
            "in a professional photo studio with a white background",
            "on a concrete floor in an industrial setting"
        ]
        
        lighting = [
            "with bright, even studio lighting",
            "with dramatic, high-contrast lighting",
            "with soft, diffused overhead lighting",
            "with warm, early morning sunlight",
            "with cool, overcast daylight",
            "under fluorescent office lights"
        ]
        
        angles = [
            "shot from a low angle",
            "shot from a high angle, looking down",
            "shot from a straight-on, eye-level perspective",
            "shot from a 45-degree angle",
            "with a slightly rotated, dutch angle",
            "as a close-up shot"
        ]

        prompt = f"{base_object}, {random.choice(environments)}, {random.choice(lighting)}, {random.choice(angles)}. professional product photography, 8k, sharp focus."
        
        return prompt
    
    async def generate_synthetic_dataset(self, golden_image_path: str, count: int) -> str:
        """Generate complete synthetic dataset with auto-labeling"""
        
        # Create dataset structure
        dataset_dir = Path("dataset")
        dataset_dir.mkdir(exist_ok=True)
        
        for split in ["train", "val"]:
            (dataset_dir / "images" / split).mkdir(parents=True, exist_ok=True)
            (dataset_dir / "labels" / split).mkdir(parents=True, exist_ok=True)
        
        # Split count between train/val
        train_count = int(count * 0.8)
        val_count = count - train_count
        
        # Generate training images
        await self._generate_split(
            golden_image_path, train_count, dataset_dir / "images" / "train",
            dataset_dir / "labels" / "train"
        )
        
        # Generate validation images  
        await self._generate_split(
            golden_image_path, val_count, dataset_dir / "images" / "val",
            dataset_dir / "labels" / "val"
        )
        
        # Create data.yaml
        self._create_data_yaml(dataset_dir)
        
        return str(dataset_dir)
    
    async def _generate_split(self, golden_image_path: str, count: int, 
                            images_dir: Path, labels_dir: Path):
        """Generate images and labels for a dataset split"""
        
        failure_count = 0
        max_failures = 10 # Abort after 10 consecutive failures

        for i in tqdm(range(count), desc=f"Generating {images_dir.parent.name} split"):
            # 1. Generate a descriptive prompt for the Bria API
            prompt = self.generate_prompt()
            
            try:
                # 2. Generate synthetic image and get the API response
                result = self.fibo_client.generate_image(prompt, source_image_path=golden_image_path)
                image_bytes = result["image_bytes"]
                api_response = result["api_response"]
                
                # 3. Save the generated image
                image_path = images_dir / f"image_{i:06d}.jpg"
                with open(image_path, "wb") as f:
                    f.write(image_bytes)
                
                # 4. Get bounding box from the API response
                bbox_data = self.fibo_client.get_bounding_box(api_response)
                
                # 5. Convert to YOLO format and save the label
                yolo_label = self._convert_to_yolo_format(bbox_data)
                label_path = labels_dir / f"image_{i:06d}.txt"
                
                with open(label_path, "w") as f:
                    f.write(yolo_label)
                
                failure_count = 0 # Reset on success

            except Exception as e:
                failure_count += 1
                print(f"❌ Failed to generate image/label for iteration {i}: {e}")
                if failure_count >= max_failures:
                    raise RuntimeError(
                        "Image generation failed too many times. "
                        "Please check your API key and network connection. "
                        f"Last error: {e}"
                    )
                continue
    
    def _convert_to_yolo_format(self, bbox_data: Dict[str, Any]) -> str:
        """Convert bounding box to YOLO format"""
        bbox = bbox_data["bbox"]  # [x1, y1, x2, y2] normalized
        
        # Convert to YOLO format: class x_center y_center width height
        x_center = (bbox[0] + bbox[2]) / 2
        y_center = (bbox[1] + bbox[3]) / 2
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        
        return f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
    
    def _create_data_yaml(self, dataset_dir: Path):
        """Create YOLO data.yaml configuration"""
        data_yaml = {
            "path": str(dataset_dir.absolute()),
            "train": "images/train",
            "val": "images/val",
            "nc": 1,
            "names": ["object"]
        }
        
        with open(dataset_dir / "data.yaml", "w") as f:
            import yaml
            yaml.dump(data_yaml, f, default_flow_style=False)
