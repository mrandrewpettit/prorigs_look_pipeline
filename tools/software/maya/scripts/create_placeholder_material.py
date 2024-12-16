import random

import maya.cmds as cmds

def get_rand_color():
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    return (r, g, b)
    
def _generate_placeholder_shading_group(mat_name):
    # TODO: check if material already exists
 
    blinn = cmds.shadingNode('blinn', name=f'tmp_{mat_name}', asShader=True)
    shadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{mat_name}')
        
    randColor = get_rand_color()
    cmds.setAttr(f'{blinn}.color', randColor[0], randColor[1], randColor[2], type='float3')
    cmds.setAttr(f'{blinn}.diffuse', 1.0)
    cmds.setAttr(f'{blinn}.specularColor', 0.0, 0.0, 0.0)
    
    cmds.connectAttr(f'{blinn}.outColor', f'{shadingGroup}.surfaceShader')
        
    print(f'[ProRigs] Successfully created "{mat_name}" placeholder material')
    cmds.confirmDialog(title='ProRigs', message=f'Successfully created "{mat_name}" placeholder material', button=["OK"])
    
    return shadingGroup
     
def create_placeholder_material():   
    result = cmds.promptDialog(
        title='Create Placeholder Material',
        message='Name of placeholder material:',
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel"
    )
    
    if result == "OK":
        mat_name = cmds.promptDialog(query=True, text=True)
    
        selected = cmds.ls(selection=True) # TODO: use type to make sure object is selected (i.e. type='transform')
        # TODO: check for selection and if none ask if user wants to still proceed
        
        shading_group = _generate_placeholder_shading_group(mat_name)
    
        cmds.select(selected, replace=True)
        cmds.sets(edit=True, forceElement=shading_group)
        
if __name__ == "__main__":
    create_placeholder_material()