import os

import maya.cmds as cmds

import utils.maya_settings as ms

def open_scene():
    """
    Opens a file dialog that defaults to the project's scenes folder, allows the user to select a scene,
    and handles unsaved changes appropriately.
    """
    project_path = cmds.workspace(q=True, rootDirectory=True)
    scene_dir = cmds.workspace(fileRuleEntry='scene')
    scene_path = os.path.join(project_path, scene_dir)
    
    file_path = cmds.fileDialog2(fileMode=1, caption="Open Scene", dir=scene_path)
    
    if file_path:
        if cmds.file(q=True, modified=True):
            result = cmds.confirmDialog(
                title="Warning: Scene Not Saved",
                message="Save changes to scene?",
                button=["Save", "Don't Save", "Cancel"],
                defaultButton="Save",
                cancelButton="Cancel",
                dismissString="Cancel"
            )
            
            if result == "Save":
                cmds.file(save=True)
            elif result == "Cancel":
                print("Open operation canceled.")
                return
            # If "Don't Save", continue to open the new scene without saving
        
        cmds.file(file_path[0], open=True, force=True)
        print(f"Scene opened: {file_path[0]}")
	
        ms.configure_scene_settings()
        ms.configure_render_settings()
    else:
        print("No file selected.")

if __name__ == "__main__":
    open_scene()