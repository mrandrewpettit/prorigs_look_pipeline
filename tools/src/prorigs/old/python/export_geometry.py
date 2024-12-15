import os
from pathlib import Path

import pymel.core as pm


def export_obj():
    script_name = 'ProRigs Export'
    asset_name = os.getenv('PR_ASSET_NAME')
    asset_type = os.getenv('PR_ASSET_TYPE')
    
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
    file_path = Path(tgt_directory) / (asset_name + '.obj')
    
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
    
    try:
        pm.system.exportSelected(file_path, type='OBJexport', force=True, options="materials=0")
        
        pm.displayInfo(f"[ProRigs] Successfully exported to {file_path}")
    except Exception as e:
        pm.displayWarning(f"[ProRigs] Failed to export: {e}")
        pm.confirmDialog(
            title=script_name,
            message=f'Failed to export: {asset_name}',
            button=["OK"]
            )