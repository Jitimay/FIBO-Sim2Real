# 🚀 FIBO-Sim2Real Factory

## Overview
End-to-end synthetic data factory using **real Bria FIBO API** for computer vision model training. Generates synthetic datasets, trains YOLOv8 models, and deploys to edge devices.

## Architecture
```
Golden Image → Real FIBO API → Synthetic Generation → Auto-Labeling → YOLOv8 Training → Edge Deployment
```

## Why FIBO is Essential
- **Real Bria FIBO API**: Uses actual FIBO text-to-image generation
- **Prompt-based control** for lighting, backgrounds, materials, angles
- **Deterministic generation** with seed control
- **Production-grade synthetic data** for robust model training

## Setup
```bash
pip install -r requirements.txt
cp .env.example .env
# Add your real Bria FIBO API key to .env
python test_fibo_connection.py  # Verify API connection
```

## Real FIBO Integration
This project uses the **actual Bria FIBO API**:
- Endpoint: `https://engine.prod.bria-api.com/v1/text-to-image/fibo`
- Authentication: Bearer token
- Input: Golden image + text prompts
- Output: High-quality synthetic variations

## Usage
1. **Generate Dataset**: `python scripts/generate_dataset.py --golden_image path/to/image.jpg --count 1000`
2. **Train Model**: `python scripts/train_model.py`
3. **Test on Real Images**: `python scripts/test_real.py --image path/to/real_image.jpg`
4. **Edge Deployment**: `python edge-demo/edge_inference.py`

## FIBO API Requirements
- Valid Bria FIBO API key
- Internet connection for API calls
- Supported image formats: JPEG, PNG
- Rate limits apply per API plan

## Project Structure
```
fibo-sim2real-factory/
├── backend/           # FastAPI server with real FIBO integration
├── frontend/          # Web UI
├── ml/               # Training pipeline
├── dataset/          # Generated datasets
├── edge-demo/        # Edge deployment
├── scripts/          # Standalone scripts
└── models/           # Trained weights
```

## Hackathon Winning Factors
- **Real FIBO API integration** - not a mock
- **Complete Sim2Real pipeline** 
- **Production-ready code**
- **Actual synthetic data generation**
- **Edge deployment capability**
