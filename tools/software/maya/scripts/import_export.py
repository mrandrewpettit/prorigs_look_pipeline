import os
from pathlib import Path
from shutil import copyfile

import maya.cmds as cmds
import pymel.core as pm

def usd_export():
    script_name = 'ProRigs Export'
    asset_name = os.getenv('PRG_ASSET_NAME')
    asset_type = os.getenv('PRG_ASSET_TYPE')
    
    selected_objs = pm.ls(selection=True, long=True, type='transform')
    selected_meshes = [
        obj for obj in selected_objs if obj.getShape() and obj.getShape().type() in ['mesh']
        ]
    
    if not selected_meshes:
        message = 'No geometry selected for export'
        pm.warning(f'[ProRigs] {message}')
        pm.confirmDialog(title=script_name, message=message, button=["OK"])
        return
    
    asset_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / asset_type / asset_name
    tgt_directory = Path(asset_directory) / 'geom'
    file_path = Path(tgt_directory) / (asset_name + '.usda')
    
    if os.path.isfile(file_path):
        result = pm.confirmDialog(
                    title=script_name,
                    message='File already exists. Overwrite?',
                    button=['OK', 'Cancel']
                    )
        if result == 'Cancel':
            pm.displayInfo(f"[ProRigs] Export cancelled.")
            return
            
    if not os.path.exists(tgt_directory):
        pm.displayInfo(f"[ProRigs] Created directory: {tgt_directory}")
        os.makedirs(tgt_directory)
    
    # TODO: have issues with writing to network drive, write now write to temp and then copy to network drive
    try:
        # Step 1: Export to a local temporary directory
        local_temp_dir = Path(pm.internalVar(userTmpDir=True)) / 'usd_exports'
        local_temp_file = local_temp_dir / (asset_name + '.usda')

        if not os.path.exists(local_temp_dir):
            os.makedirs(local_temp_dir)
        
        cmds.mayaUSDExport(file=str(local_temp_file), exportDisplayColor=True, defaultUSDFormat='usda', kind='group', selection=True)
        
        # Step 2: Copy the exported file to the network target directory
        copyfile(local_temp_file, file_path)
        
        pm.displayInfo(f"[ProRigs] Successfully exported to {file_path}")
    except Exception as e:
        pm.displayWarning(f"[ProRigs] Failed to export: {e}")
        pm.confirmDialog(
            title=script_name,
            message=f'Failed to export: {asset_name}\nError: {e}',
            button=["OK"]
        )

def usd_import():
    script_name = 'ProRigs Export'
    asset_name = os.getenv('PRG_ASSET_NAME')
    asset_type = os.getenv('PRG_ASSET_TYPE')
    
    asset_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / asset_type / asset_name
    tgt_directory = Path(asset_directory) / 'geom'
    file_path = Path(tgt_directory) / (asset_name + '.usda')
    
    if not os.path.isfile(file_path):
        # TODO: convert this to an exception to be caught
        cmds.confirmDialog(title='ProRigs', message=f'Working {asset_name} usd file does not exist. Please create before trying again', button=["OK"]) # TODO: dynamically add title
        print(f'[ProRigs] Error: failed to import {asset_name}. Working USD file does not exist here: {file_path}')
        return
    
    cmds.mayaUSDImport(file=file_path, preferredMaterial='blinn')