import sys
import pkg_resources
import cv2
import os

def check_requirements():
    required = {
        'torch': '2.0.0',
        'opencv-python-headless': '4.8.1',
        'ultralytics': '8.0.0',
        'matplotlib': '3.8.0',
        'numpy': '1.26.0'
    }
    
    missing = []
    outdated = []
    
    for package, min_version in required.items():
        try:
            installed = pkg_resources.get_distribution(package)
            if pkg_resources.parse_version(installed.version) < pkg_resources.parse_version(min_version):
                outdated.append(f"{package} (installed: {installed.version}, required: {min_version})")
        except pkg_resources.DistributionNotFound:
            missing.append(package)
    
    return missing, outdated

def check_camera():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False
        cap.release()
        return True
    except:
        return False

def check_system():
    print("Checking system requirements...")
    print("-" * 50)
    
    # Check Python version
    print(f"Python version: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
    else:
        print("✅ Python version OK")
    
    # Check packages
    missing, outdated = check_requirements()
    if not missing and not outdated:
        print("✅ All required packages are installed and up to date")
    else:
        if missing:
            print("❌ Missing packages:")
            for package in missing:
                print(f"   - {package}")
        if outdated:
            print("⚠️ Outdated packages:")
            for package in outdated:
                print(f"   - {package}")
    
    # Check camera
    if check_camera():
        print("✅ Camera is accessible")
    else:
        print("❌ Camera is not accessible")
    
    # Check disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage("/")
        free_gb = free // (2**30)
        print(f"✅ Free disk space: {free_gb}GB")
        if free_gb < 5:
            print("⚠️ Low disk space warning")
    except:
        print("⚠️ Could not check disk space")

def main():
    check_system()

if __name__ == "__main__":
    main() 