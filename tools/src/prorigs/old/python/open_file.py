import os
from pathlib import Path

from maya.api.OpenMaya import MSceneMessage
import maya.cmds as cmds
import pymel.core as pm

def open_working_file():
    asset_name = os.getenv('PR_ASSET_NAME')
    #TODO copied the line below from export_geometry
    asset_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / os.getenv('PR_ASSET_TYPE') / asset_name
    asset_geom_file = Path(asset_directory) / 'geom' / (asset_name + '.obj')
        
    if os.path.isfile(asset_geom_file):
        try:
            pm.system.importFile(
                asset_geom_file, 
                type='OBJ',  # Specify file type (can be 'FBX', 'mayaAscii', etc.)
                namespace=':',  # Handle namespace conflicts
                ignoreVersion=True, 
            )
            pm.displayInfo(f"[ProRigs] Successfully imported: {asset_geom_file}")
        except Exception as e:
            pm.displayWarning(f"[ProRigs] Failed to import: {e}")
    else:
        pass
        # TODO: dialog box
        pm.displayWarning(f'[ProRigs] Working file or geom file doesn not exist for {asset_name}. Must generate a obj file first')


        """
        def open_working_file():
    asset_name = os.getenv('PR_ASSET_NAME')
    #TODO copied the line below from export_geometry
    asset_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / os.getenv('PR_ASSET_TYPE') / asset_name
    asset_maya_directory = Path(asset_directory) / 'maya'
    asset_working_file = Path(asset_maya_directory) / (asset_name + '.ma')
    asset_geom_file = Path(asset_directory) / 'geom' / (asset_name + '.obj')
        
    if os.path.isfile(asset_working_file):
        pm.openFile(asset_working_file)
        pm.displayInfo(f"Opened file: {asset_working_file}")
    elif os.path.isfile(asset_geom_file):
        try:
            pm.system.importFile(
                asset_geom_file, 
                type='OBJ',  # Specify file type (can be 'FBX', 'mayaAscii', etc.)
                namespace=':',  # Handle namespace conflicts
                ignoreVersion=True, 
            )
            pm.displayInfo(f"[ProRigs] Successfully imported: {asset_geom_file}")
            pm.renameFile(asset_working_file)
            pm.saveFile()
            pm.displayInfo(f"[ProRigs] Working file saved to: {asset_working_file}")
        except Exception as e:
            pm.displayWarning(f"[ProRigs] Failed to import: {e}")
    else:
        pass
        # TODO: dialog box
        pm.displayWarning(f'[ProRigs] Working file or geom file doesn not exist for {asset_name}. Must generate a obj file first')
        """
      
#def on_scene_ready(*args):
#    print('READY TO GO AGAIN!')
#MSceneMessage.addCallback(MSceneMessage.kAfterOpen, on_scene_ready)
