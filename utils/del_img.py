import os
from pathlib import Path

def delete_images_recursively(directory_path):
    """Recursively deletes .jpg, .jpeg, and .png files in the specified directory."""
    
    target_dir = Path(directory_path)
    if not target_dir.is_dir():
        print(f"Error: Directory not found at '{directory_path}'")
        return

    print(f"Scanning and deleting images in: {target_dir}")
    deleted_count = 0

    extensions = ('*.jpg', '*.jpeg', '*.png')

    for ext in extensions:
        for file_path in target_dir.glob(f'**/{ext}'):
            try:
                os.remove(file_path)
                print(f"  > Deleted: {file_path.name}") 
                deleted_count += 1
            except OSError as e:
                print(f"  > Error deleting {file_path.name}: {e}")

    print("-" * 30)
    print(f"Finished. Total images deleted: {deleted_count}")

target_directory = '../assets/images/team/'
delete_images_recursively(target_directory)