import os

import maya.cmds as cmds

def toggle_reference(file_path, namespace):
    ref_nodes = cmds.ls(type="reference")
    for ref_node in ref_nodes:
        try:
            ref_file = cmds.referenceQuery(ref_node, filename=True)
            if os.path.normpath(ref_file) == os.path.normpath(file_path):
                cmds.file(ref_file, removeReference=True)
                print(f"Removed reference: {file_path}")
                return
        except RuntimeError:
            # Some references might not have file paths, ignore them
            continue

    # If the reference is not found, add it
    cmds.file(
        file_path,
        reference=True,
        type="mayaAscii",
        ignoreVersion=True,
        namespace=namespace
    )
    print(f"Referenced file: {file_path}")