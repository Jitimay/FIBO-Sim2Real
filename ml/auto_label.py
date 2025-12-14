#!/usr/bin/env python3
"""
Auto-labeling utilities for synthetic datasets
"""
import cv2
import numpy as np
from typing import List, Dict, Tuple
import json

class AutoLabeler:
    def __init__(self):
        pass
    
    def generate_bbox_from_mask(self, mask: np.ndarray) -> Dict[str, float]:
        """Generate bounding box from segmentation mask"""
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None
        
        # Get largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Convert to normalized coordinates
        height, width = mask.shape
        
        return {
            'x1': x / width,
            'y1': y / height,
            'x2': (x + w) / width,
            'y2': (y + h) / height,
            'confidence': 1.0,
            'class': 'object'
        }
    
    def generate_segmentation_mask(self, image: np.ndarray, bbox: Dict[str, float]) -> np.ndarray:
        """Generate segmentation mask from bounding box (simple approach)"""
        height, width = image.shape[:2]
        
        # Convert normalized bbox to pixel coordinates
        x1 = int(bbox['x1'] * width)
        y1 = int(bbox['y1'] * height)
        x2 = int(bbox['x2'] * width)
        y2 = int(bbox['y2'] * height)
        
        # Create mask
        mask = np.zeros((height, width), dtype=np.uint8)
        mask[y1:y2, x1:x2] = 255
        
        return mask
    
    def convert_to_yolo_format(self, bbox: Dict[str, float]) -> str:
        """Convert bounding box to YOLO format"""
        x_center = (bbox['x1'] + bbox['x2']) / 2
        y_center = (bbox['y1'] + bbox['y2']) / 2
        width = bbox['x2'] - bbox['x1']
        height = bbox['y2'] - bbox['y1']
        
        return f"0 {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"
    
    def convert_to_coco_format(self, bbox: Dict[str, float], image_id: int, 
                              annotation_id: int) -> Dict:
        """Convert to COCO format"""
        return {
            "id": annotation_id,
            "image_id": image_id,
            "category_id": 1,
            "bbox": [bbox['x1'], bbox['y1'], 
                    bbox['x2'] - bbox['x1'], bbox['y2'] - bbox['y1']],
            "area": (bbox['x2'] - bbox['x1']) * (bbox['y2'] - bbox['y1']),
            "iscrowd": 0
        }
    
    def validate_annotation(self, bbox: Dict[str, float]) -> bool:
        """Validate bounding box annotation"""
        if not all(key in bbox for key in ['x1', 'y1', 'x2', 'y2']):
            return False
        
        if bbox['x1'] >= bbox['x2'] or bbox['y1'] >= bbox['y2']:
            return False
        
        if not (0 <= bbox['x1'] <= 1 and 0 <= bbox['y1'] <= 1 and
                0 <= bbox['x2'] <= 1 and 0 <= bbox['y2'] <= 1):
            return False
        
        return True
