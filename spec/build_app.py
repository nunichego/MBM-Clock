#!/usr/bin/env python
"""
Build script for creating an executable from the Mind Before Machine timer app.
This script handles common PyInstaller issues with PyQt5 applications.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_ico_if_missing():
    """Create an .ico file from a PNG if needed"""
    try:
        from PIL import Image
        
        # Check if icon.ico exists in resources/icons
        icon_path = Path('resources/icons/icon.ico')
        if icon_path.exists():
            print("Icon file already exists.")
            return
        
        # Look for PNG files to convert
        png_files = list(Path('resources/icons').glob('*.png'))
        if not png_files:
            print("No PNG files found to convert to ICO.")
            return
            
        # Use the first PNG file
        png_path = png_files[0]
        print(f"Converting {png_path} to {icon_path}")
        
        # Create directory if it doesn't exist
        icon_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert PNG to ICO
        img = Image.open(png_path)
        img.save(icon_path)
        print(f"Created {icon_path}")
        
    except ImportError:
        print("Pillow not installed. Cannot create ICO file.")
        print("Install with: pip install pillow")
    except Exception as e:
        print(f"Error creating ICO file: {e}")

def clean_build_directories():
    """Remove build and dist directories if they exist"""
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name} directory...")
            shutil.rmtree(dir_name)

def run_pyinstaller():
    """Run PyInstaller with the spec file"""
    cmd = ['pyinstaller', 'timer_app.spec']
    print("Running PyInstaller...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print("PyInstaller stdout:")
    print(result.stdout)
    
    if result.stderr:
        print("PyInstaller stderr:")
        print(result.stderr)
    
    return result.returncode == 0

def copy_resources_if_needed():
    """Check if resources exists in the dist directory, copy if missing"""
    dist_resources = Path('dist/Mind_Before_Machine/resources')
    if not dist_resources.exists():
        print("Resources directory not found in dist, copying manually...")
        shutil.copytree('resources', dist_resources)

def main():
    """Main build function"""
    print("Starting build process...")
    
    # Create ico file if needed
    create_ico_if_missing()
    
    # Clean build directories
    clean_build_directories()
    
    # Run PyInstaller
    success = run_pyinstaller()
    
    if success:
        # Copy resources if needed
        copy_resources_if_needed()
        print("\nBuild completed successfully!")
        print("Executable can be found in: dist/Mind_Before_Machine/Mind_Before_Machine.exe")
    else:
        print("\nBuild failed. Check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())