import os
import re
from pathlib import Path

import maya.cmds as cmds

#TODO: CLEANUP EVERYTHING BELOW
def flush_arnold_textures():
    try:
        # Clear all texture caches in Arnold
        cmds.arnoldFlushCache( textures=True )
        print("All Arnold textures have been flushed.")
    except Exception as e:
        print(f"Failed to flush textures: {e}")

def locate_file(folder_path, asset_name, key):
    # Define the regex pattern to match the new key and .tif extension
    pattern = re.compile(rf"{asset_name}_{key}\.\d{{4}}\.tif", re.IGNORECASE)

    # Get the list of files in the specified folder (no subdirectories)
    files = os.listdir(folder_path)

    # Search through the list of files for matching filenames
    for file_name in files:
        if pattern.match(file_name):
            return file_name  # Return only the filename

    return None

def get_specific_shading_nodes():
    node_types = ['file']  # Add more if needed
    shading_nodes = []
    for node_type in node_types:
        nodes = cmds.ls(type=node_type)
        shading_nodes.extend(nodes)
    return shading_nodes

def update_textures():
    flush_arnold_textures()
    
    asset_name = os.getenv('PRG_ASSET_NAME')
    asset_type = os.getenv('PRG_ASSET_TYPE')
    asset_tex_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / asset_type / asset_name / 'sourceimages'
    
    shading_nodes = get_specific_shading_nodes()
    
    for node in shading_nodes:
        asset_name = os.getenv('PRG_ASSET_NAME')
        key = node[2:]
        
        file_path = locate_file(asset_tex_directory, asset_name, key)
        file_path = Path('sourceimages') / file_path
        
        cmds.setAttr(f'{node}.fileTextureName', file_path, type='string')
        cmds.setAttr(f'{node}.ignoreColorSpaceFileRules', 1)
        if key.split('_')[-1].lower() != 'basecolor':
            cmds.setAttr(f'{node}.colorSpace', 'Raw', type='string')
        else:
            cmds.setAttr(f'{node}.colorSpace', 'sRGB', type='string')
        
if __name__ == "__main__":
    update_textures()