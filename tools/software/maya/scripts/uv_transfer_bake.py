import maya.cmds as cmds
import maya.mel as mel

def uv_transfer_bake():
    selection = cmds.ls(selection=True)
    if len(selection) != 2:
        cmds.warning("Please select exactly two groups.")
        return
    
    src, tgt = selection
    src_geos = cmds.listRelatives(src, allDescendents=True, type="mesh", fullPath=True) or []
    tgt_geos = cmds.listRelatives(tgt, allDescendents=True, type="mesh", fullPath=True) or []
    
    if not src_geos or not tgt_geos:
        cmds.warning("One or both groups have no geometry.")
        return
    
    # Convert mesh nodes to their transform nodes and strip the root group name
    def get_short_name_mapping(meshes):
        mapping = {}
        for geo in meshes:
            transform = cmds.listRelatives(geo, parent=True, fullPath=True)[0]  # Get transform node
            short_name = transform.split("|")[-1]  # Short name of the geometry
            mapping[short_name] = transform  # Map short name to transform node
        return mapping
    
    src_mapping = get_short_name_mapping(src_geos)
    tgt_mapping = get_short_name_mapping(tgt_geos)
    
    # Loop through source selection meshes and find matching names in target selection
    for src_name, src_transform in src_mapping.items():
        if src_name in tgt_mapping:
            tgt_transform = tgt_mapping[src_name]
            print(f"Transferring UVs from '{src_transform}' to '{tgt_transform}'...")
            try:
                cmds.polyTransfer(tgt_transform, uv=1, ao=src_transform)
                cmds.select(tgt_transform)
                mel.eval('doBakeNonDefHistory(1, {"prePost"});')
            except Exception as e:
                cmds.warning(f"Error transferring UVs for {src_transform}: {e}")
        else:
            cmds.warning(f"No matching geometry found in group2 for '{src_name}'.")

    print("UV transfer completed.")

if __name__ == "__main__":
    uv_transfer_bake()