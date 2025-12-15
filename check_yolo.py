#!/usr/bin/env python3
"""
Check if YOLO/Ultralytics is properly installed
"""

def check_yolo_installation():
    print("🔍 Checking YOLO/Ultralytics installation...")
    
    try:
        import ultralytics
        print(f"✅ Ultralytics version: {ultralytics.__version__}")
        
        from ultralytics import YOLO
        print("✅ YOLO import successful")
        
        # Try to load a model
        try:
            model = YOLO('yolov8n.pt')
            print("✅ YOLOv8n model loaded successfully")
            print(f"📊 Model info: {model.info()}")
            return True
        except Exception as e:
            print(f"⚠️ Model loading failed: {e}")
            print("💡 This might be normal on first run (model will download)")
            return True
            
    except ImportError as e:
        print(f"❌ Ultralytics not installed: {e}")
        print("🔧 Install with: pip install ultralytics")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_torch():
    print("\n🔍 Checking PyTorch installation...")
    
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        print(f"🖥️ CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"🎮 CUDA device: {torch.cuda.get_device_name(0)}")
        return True
    except ImportError:
        print("❌ PyTorch not installed")
        print("🔧 Install with: pip install torch torchvision")
        return False

def check_other_deps():
    print("\n🔍 Checking other dependencies...")
    
    deps = ['PIL', 'cv2', 'numpy', 'yaml']
    all_good = True
    
    for dep in deps:
        try:
            if dep == 'PIL':
                from PIL import Image
                print("✅ Pillow (PIL)")
            elif dep == 'cv2':
                import cv2
                print(f"✅ OpenCV version: {cv2.__version__}")
            elif dep == 'numpy':
                import numpy as np
                print(f"✅ NumPy version: {np.__version__}")
            elif dep == 'yaml':
                import yaml
                print("✅ PyYAML")
        except ImportError:
            print(f"❌ {dep} not installed")
            all_good = False
    
    return all_good

def main():
    print("🚀 FIBO-Sim2Real Factory - Dependency Check")
    print("=" * 50)
    
    yolo_ok = check_yolo_installation()
    torch_ok = check_torch()
    deps_ok = check_other_deps()
    
    print("\n📋 Summary:")
    print(f"YOLO/Ultralytics: {'✅' if yolo_ok else '❌'}")
    print(f"PyTorch: {'✅' if torch_ok else '❌'}")
    print(f"Other deps: {'✅' if deps_ok else '❌'}")
    
    if yolo_ok and torch_ok and deps_ok:
        print("\n🎉 All dependencies are ready!")
        print("🚀 You can now run: python quick_fix_server.py")
    else:
        print("\n⚠️ Some dependencies are missing.")
        print("🔧 Install missing packages with:")
        if not torch_ok:
            print("   pip install torch torchvision")
        if not yolo_ok:
            print("   pip install ultralytics")
        if not deps_ok:
            print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()