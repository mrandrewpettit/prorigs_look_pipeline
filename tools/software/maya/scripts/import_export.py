import os
from pathlib import Path
from shutil import copyfile

import maya.cmds as cmds
import pymel.core as pm

#TODO: CLEANUP
def _duplicate_sel_hierarchy(selection, root_name):
    # Step 1: Trace hierarchy up to the root
    root_to_sel = []
    
    iter = 0
    current_node = selection
    while current_node:
        if iter > 0:
            root_to_sel.insert(0, current_node)
        parent_node = cmds.listRelatives(current_node, parent=True, fullPath=True)
        current_node = parent_node[0] if parent_node else None
        iter = iter + 1
        
    # Step 2: Recreate the root_to_sel heirarchy
    prev_group = None
    for i, group in enumerate(root_to_sel):
        new_group_name = group.split("|")[-1] if i > 0 else root_name #group.split("|")[-1] + '_duplicate'
        new_group = cmds.group(empty=True, name=new_group_name)

        if prev_group:
            new_group = cmds.parent(new_group, prev_group)

        prev_group = new_group
    duplicate_group_root = prev_group
    
    # Step 3: Duplicate selection and parent to new toor_to_sel heirarchy
    new_sel = cmds.duplicate(selection)
    new_sel = cmds.parent(new_sel[0], duplicate_group_root)[0]
    cmds.rename(new_sel, new_sel[:-1])

    return duplicate_group_root
    
#TODO: CLEANUP
def _get_group_geo(selection):
    # This function returns all geometry (mesh nodes) within the selected group(s)
    geo = []
    children = cmds.listRelatives(selection, allDescendents=True, fullPath=True, type='transform') or []
    for child in children:
        if cmds.listRelatives(child, shapes=True, type='mesh'):
            geo.append(child)
    return geo

#TODO: CLEANUP
def fbx_export():
    # Step 0: calculate export paths
    asset_name = os.getenv('PRG_ASSET_NAME')
    asset_type = os.getenv('PRG_ASSET_TYPE')
        
    asset_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / asset_type / asset_name
    tgt_directory = Path(asset_directory) / 'geom'
    low_path = Path(tgt_directory) / (asset_name + '.fbx')
    high_path = Path(tgt_directory) / 'substance' / (asset_name + '.fbx')
    
    # Step 1: Get selection
    selection = cmds.ls(selection=True, long=True)[0]
    if not selection:
        cmds.warning("Nothing is selected. Please select a group or geometry to export.")
        return

    # TODO: check if any descendants in selection are actually geometry

    # Step 2: Duplicate hierarchy and get cleaned geometry
    duplicate_group = _duplicate_sel_hierarchy(selection, asset_name + '_static')

    # Step 3: Clean up geometry
    duplicate_geo = _get_group_geo(duplicate_group)
    #cmds.delete(duplicate_group, constructionHistory=True)
        
    for geo in duplicate_geo:
        # Extract the base name and duplicate
        geo_name = cmds.ls(geo, shortNames=True)[0]
        cmds.delete(geo_name, constructionHistory=True)
    
    # Step 4: Export low-res FBX
    # TODO: fix to remove export constraint warnings
    try:
        cmds.select(duplicate_group, replace=True)
        cmds.file(low_path, force=True, options="v=0;", type="FBX export", preserveReferences=True, exportSelected=True)    
        print(f"Low-res FBX exported to: {low_path}")
    except Exception as e:
        cmds.warning(f"Failed to export low-res FBX: {e}")
        return
        
    # Step 5: Duplicate for high-res and apply subdivisions
    for geo in duplicate_geo:
        geo_name = cmds.ls(geo, shortNames=True)[0].split('|')[-1]
        high_res_geo = cmds.rename(geo, geo_name + '_high')
        cmds.polySmooth(high_res_geo, divisions=2, keepBorder=False)
    
    # Step 6: Export high-res FBX
    # TODO: fix to remove export constraint warnings
    try:
        cmds.select(duplicate_group, replace=True)
        cmds.file(high_path, force=True, options="v=0;", type="FBX export", preserveReferences=True, exportSelected=True)    
        print(f"High-res FBX exported to: {low_path}")
    except Exception as e:
        cmds.warning(f"Failed to export high-res FBX: {e}")
        return
        
    # Step 7: Cleanup
    cmds.delete(duplicate_group)
    print("Cleaned up duplicated hierarchy and geometry.")

#TODO: CLEANUP
def fbx_import():
    asset_name = os.getenv('PRG_ASSET_NAME')
    asset_type = os.getenv('PRG_ASSET_TYPE')
    
    asset_directory = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / asset_type / asset_name
    tgt_directory = Path(asset_directory) / 'geom'
    fbx_file = Path(tgt_directory) / (asset_name + '.fbx')
    
    # Step 1: Ask the user if they want to import with materials
    import_with_materials = cmds.confirmDialog(
        title="Import with Materials",
        message="Do you want to import the FBX with materials?",
        button=["Yes", "No"],
        defaultButton="Yes",
        cancelButton="No",
        dismissString="No"
    )

    # Step 2: Get a list of existing geometry and shading groups
    existing_geometry = set(cmds.ls(geometry=True, long=True))
    existing_shading_groups = set(cmds.ls(type='shadingEngine'))

    # Step 3: Import the FBX file
    try:
        cmds.file(fbx_file, i=True, type="FBX", ignoreVersion=True, mergeNamespacesOnClash=False, namespace="importedFBX")
        print(f"Successfully imported: {fbx_file}")
    except Exception as e:
        print(f"Failed to import FBX file: {e}")
        return

    # Step 4: Identify the newly imported geometry
    all_geometry = set(cmds.ls(geometry=True, long=True))
    new_geometry = all_geometry - existing_geometry
    print(f"New geometry nodes: {new_geometry}")

    # Step 5: Find shading groups attached to the new geometry
    new_shading_groups = set()
    for geo in new_geometry:
        shading_groups = cmds.listConnections(geo, type="shadingEngine") or []
        new_shading_groups.update(shading_groups)
    print(f"New shading groups: {new_shading_groups}")

    # Step 6: Identify materials connected to these new shading groups
    new_materials = set()
    for sg in new_shading_groups:
        materials = cmds.listConnections(f"{sg}.surfaceShader", source=True) or []
        new_materials.update(materials)
    print(f"New materials: {new_materials}")

    # Step 7: Delete the identified materials and shading engines only if the user chose "No" (not to import materials)
    if import_with_materials == "No" and new_materials:
        cmds.delete(list(new_materials))  # Delete materials
        print(f"Deleted materials: {new_materials}")
        
        # Also delete the associated shading engines
        cmds.delete(list(new_shading_groups))  # Delete shading engines
        print(f"Deleted shading engines: {new_shading_groups}")
    else:
        print("No materials or shading engines deleted.")

    # Step 8: Assign 'lambert1' material to the newly imported geometry only if materials are not imported
    if import_with_materials == "No" and new_geometry:
        lambert1_shading_group = "initialShadingGroup"  # Shading group connected to lambert1
        cmds.sets(list(new_geometry), e=True, forceElement=lambert1_shading_group)
        print("Assigned 'lambert1' to the new geometry.")
    else:
        print("No new geometry found to assign 'lambert1'.")

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
        
        cmds.mayaUSDExport(file=str(local_temp_file), defaultUSDFormat='usda', kind='group', selection=True)
        
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
    
    result = pm.confirmDialog(
            title=script_name,
            message='Import display colors as materials?',
            button=['Yes', 'No']
            )
    if result == 'Yes':
        cmds.mayaUSDImport(file=file_path, preferredMaterial='blinn')
    if result == 'No':
        cmds.mayaUSDImport(file=file_path, shadingMode=('none', ''))