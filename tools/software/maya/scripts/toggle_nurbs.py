import maya.cmds as cmds

def toggle_nurbs():
    panels = cmds.getPanel(type="modelPanel")
    
    if not panels:
        print("No active viewports found.")
        return
    
    for panel in panels:
        # Check the current state of NURBS curves and surfaces visibility
        curves_state = cmds.modelEditor(panel, query=True, nurbsCurves=True)
        surfaces_state = cmds.modelEditor(panel, query=True, nurbsSurfaces=True)
    
        # Toggle the visibility state
        cmds.modelEditor(panel, edit=True, nurbsCurves=not curves_state)
        cmds.modelEditor(panel, edit=True, nurbsSurfaces=not surfaces_state)

if __name__ == "__main__":
    toggle_nurbs()