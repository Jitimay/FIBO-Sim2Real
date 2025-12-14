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
        
    def generate_variation_params(self) -> Dict[str, Any]:
        """Generate random variation parameters for FIBO"""
        return {
            "seed": random.randint(1, 1000000),
            "azimuth": random.uniform(-180, 180),
            "elevation": random.uniform(-30, 60),
            "distance": random.uniform(0.5, 2.0),
            "fov": random.uniform(30, 70),
            "light_intensity": random.uniform(0.5, 1.5),
            "light_angle": random.uniform(0, 90),
            "roughness": random.uniform(0.1, 0.9),
            "metallic": random.uniform(0.0, 0.3),
            "background": random.choice([
                "industrial", "outdoor", "lab", "neutral", "warehouse"
            ]),
            "noise": random.uniform(0.0, 0.1)
        }
    
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
        
        for i in tqdm(range(count), desc="Generating images"):
            # Generate variation parameters
            params = self.generate_variation_params()
            
            # Generate synthetic image using FIBO
            image_bytes = self.fibo_client.generate_image(golden_image_path, params)
            
            # Save image
            image_path = images_dir / f"image_{i:06d}.jpg"
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            
            # Get bounding box from FIBO
            bbox_data = self.fibo_client.get_bounding_box(image_bytes)
            
            # Convert to YOLO format and save label
            yolo_label = self._convert_to_yolo_format(bbox_data)
            label_path = labels_dir / f"image_{i:06d}.txt"
            
            with open(label_path, "w") as f:
                f.write(yolo_label)
    
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
