import os
from pathlib import Path

import maya.cmds as cmds
import pymel.core as pm

def usd_export():
    script_name = 'ProRigs Export'
    asset_name = os.getenv('PR_ASSET_NAME')
    asset_type = os.getenv('PR_ASSET_TYPE')
    
    asset_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / asset_type / asset_name
    tgt_directory = Path(asset_directory) / 'geom'
    file_path = Path(tgt_directory) / (asset_name + '.usda')
    
    if not os.path.isfile(file_path):
        # TODO: convert this to an exception to be caught
        cmds.confirmDialog(title='ProRigs', message=f'Working {asset_name} usd file does not exist. Please create before trying again', button=["OK"]) # TODO: dynamically add title
        print(f'[ProRigs] Error: failed to import {asset_name}. Working USD file does not exist here: {file_path}')
        return
    
    cmds.mayaUSDImport(file=file_path, preferredMaterial='blinn')

    """
    try:
        
        pm.displayInfo(f"[ProRigs] Successfully imported from {file_path}")
    except Exception as e:
        pm.displayWarning(f"[ProRigs] Failed to export: {e}")
        pm.confirmDialog(
            title=script_name,
            message=f'Failed to export: {asset_name}',
            button=["OK"]
        )
    """
            
    
usd_export()

