import os
import shutil

import maya.cmds as cmds

#assign texture files to file nodes
#check  that all texture maps are teh right color
# baseColor
# roughness
# metalness
# height
# normal


def flush_arnold_textures():
    try:
        # Clear all texture caches in Arnold
        cmds.arnoldFlushCache( textures=True )
        print("All Arnold textures have been flushed.")
    except Exception as e:
        print(f"Failed to flush textures: {e}")
    
def move_all_files(src_folder, dest_folder):
    # Ensure the source and destination folders exist
    if not os.path.exists(src_folder):
        raise FileNotFoundError(f"Source folder not found: {src_folder}")
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Create destination folder if it doesn't exist

    # Iterate over all files in the source folder
    for filename in os.listdir(src_folder):
        src_file = os.path.join(src_folder, filename)
        dest_file = os.path.join(dest_folder, filename)

        # If the file already exists in the destination, remove it
        if os.path.exists(dest_file):
            os.remove(dest_file)

        # Move the file
        shutil.move(src_file, dest_folder)

    print(f"All files moved from {src_folder} to {dest_folder}.")

# Example usage
#src = "path/to/source/folder"
#dest = "path/to/destination/folder"

flush_arnold_textures()

asset_name = os.getenv('PR_ASSET_NAME')
asset_type = os.getenv('PR_ASSET_TYPE')
asset_tex_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / asset_type / asset_name / 'tex'
tgt_directory = os.getenv('PRG_MAYA_SOURCEIMAGES')

move_all_files(asset_tex_directory, tgt_directory)
