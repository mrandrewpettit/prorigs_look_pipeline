import os
import shutil
import argparse
import sys

def validate_directory(path, description):
    if not os.path.isdir(path):
        print(f"Error: {description} does not exist: {path}")
        sys.exit(1)

def find_ma_file(directory):
    for file in os.listdir(directory):
        if file.endswith(".ma"):
            return file
    return None

def move_files(source_dir, target_dir):
    validate_directory(source_dir, "Source directory")
    validate_directory(target_dir, "Target directory")
    
    # Define target directories
    scenes_dir = os.path.join(target_dir, "scenes")
    sourceimages_dir = os.path.join(target_dir, "sourceimages")
    
    # Ensure target subdirectories exist
    validate_directory(scenes_dir, "Scenes directory")
    validate_directory(sourceimages_dir, "Sourceimages directory")
    
    # Locate and move the .ma file
    ma_file = find_ma_file(source_dir)
    if not ma_file:
        print("Error: No .ma file found in the source directory.")
        sys.exit(1)
    
    shutil.move(os.path.join(source_dir, ma_file), os.path.join(scenes_dir, ma_file))
    print(f"Moved {ma_file} to {scenes_dir}")
    
    # Verify texture directory and move image files
    textures_dir = os.path.join(source_dir, 
                                "sourceImages_DO_NOT_RENAME_OR_REPATH")
    if not os.path.isdir(textures_dir):
        print("Warning: 'sourceImages_DO_NOT_RENAME_OR_REPATH' directory is missing.")
        return
    
    image_files = [
        f for f in os.listdir(textures_dir) 
        if os.path.isfile(os.path.join(textures_dir, f))
    ]
    if not image_files:
        print("Warning: 'sourceImages_DO_NOT_RENAME_OR_REPATH' directory contains no images.")
        return
    
    for file in image_files:
        src_path = os.path.join(textures_dir, file)
        dest_path = os.path.join(sourceimages_dir, file)
        
        if not file.lower().endswith((".tif", ".tiff")):
            print(f"Warning: Non-TIFF image file detected: {file}")
            continue
        
        shutil.move(src_path, dest_path)
        print(f"Moved {file} to {sourceimages_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Move a Maya project and textures to the target directory."
    )
    parser.add_argument(
        "source_dir", 
        help="Path to the source directory containing the .ma file and textures folder."
    )
    parser.add_argument(
        "--target_dir", 
        default="W:/prorigs/prorigs_look_pipeline_DEV/tools/software/maya/projects/default", 
        help="Path to the target Maya project directory "
             "(default: W:/prorigs/prorigs_look_pipeline_DEV/tools/software/maya/projects/default)"
    )
    args = parser.parse_args()
    
    move_files(args.source_dir, args.target_dir)
