import pathlib
from PIL import Image
import os  # Keep for debugging

def convert_jpegs_to_webp(quality=85):
    """
    Converts all JPEG images in the current directory to WebP format, 
    handling various case extensions (e.g., .JPG, .jpeg, .JPeG).
    """
    # Define all possible JPEG extensions
    JPEG_EXTENSIONS = {'.jpg','.jpeg'}
    
    # Get the current working directory
    current_dir = pathlib.Path('.')
    current_dir_abs = current_dir.absolute()
    
    print(f"📁 Current directory: {current_dir_abs}")
    print(f"📁 Directory exists: {current_dir_abs.exists()}")
    
    # List all files in directory for debugging
    all_files = list(current_dir.iterdir())
    print(f"🔍 Found {len(all_files)} items in directory:")
    
    for item in all_files:
        if item.is_file():
            print(f"   📄 {item.name} (suffix: {item.suffix}, lower: {item.suffix.lower()})")
    
    # Filter JPEG files
    jpeg_files = []
    for item in current_dir.iterdir():
        if item.is_file() and item.suffix.lower() in JPEG_EXTENSIONS:
            jpeg_files.append(item)
    
    print(f"\n✅ Found {len(jpeg_files)} JPEG images to convert:")
    for jpeg in jpeg_files:
        print(f"   • {jpeg.name}")
    
    if not jpeg_files:
        print("\n❌ No JPEG images found. Possible issues:")
        print("   - JPEG files might have different extensions (e.g., .JPG, .JPEG)")
        print("   - The script is running in a different directory than expected")
        print("   - File permissions might be preventing access")
        print("   - Try running the script from the command line in the image directory")
        return
    
    # Conversion loop
    for input_path in jpeg_files:
        try:
            with Image.open(input_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                output_path = input_path.with_suffix('.webp')
                
                if output_path.exists():
                    print(f"⏩ Skipping: {output_path.name} already exists.")
                    continue
                
                img.save(output_path, 'webp', quality=quality)
                print(f"✨ Converted '{input_path.name}' to '{output_path.name}'")
                
        except Exception as e:
            print(f"🛑 Error converting {input_path.name}: {e}")
    
    print("\n🎉 Conversion complete.")


if __name__ == "__main__":
    # Check if Pillow is properly installed
    try:
        convert_jpegs_to_webp(quality=90)
    except ImportError:
        print("❌ Pillow (PIL) is not installed. Install it with: pip install Pillow")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")