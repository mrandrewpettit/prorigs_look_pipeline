import random

def get_rand_color():
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    return (r, g, b)
    
def add_placeholder_material(mat_name):
    # TODO: check if material already exists
 
    blinn = cmds.shadingNode('blinn', name=f'tmp_{mat_name}', asShader=True)
    shadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{mat_name}')
        
    randColor = get_rand_color()
    cmds.setAttr(f'{blinn}.color', randColor[0], randColor[1], randColor[2], type='float3')
    cmds.setAttr(f'{blinn}.diffuse', 1.0)
    cmds.setAttr(f'{blinn}.specularColor', 0.0, 0.0, 0.0)
    
    cmds.connectAttr(f'{blinn}.outColor', f'{shadingGroup}.surfaceShader')
        
    print(f'[ProRigs] Successfully added "{mat_name}" placeholder material')
    cmds.confirmDialog(title='ProRigs', message=f'Successfully added "{mat_name}" placeholder material', button=["OK"]) # TODO: dynamically add title
    
    return shadingGroup
      
try:    
    result = cmds.promptDialog(
        title='ProRigs Create Material',
        message='Name of material:',
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel"
    ) # TODO: dynamically add title/message

    if result == "OK":
        mat_name = cmds.promptDialog(query=True, text=True)
   
        selected = cmds.ls(selection=True) # TODO: use type to make sure object is selected (i.e. type='transform')
        # TODO: check for selection and if none ask if user wants to still proceed
        
        shading_group = add_placeholder_material(mat_name)

        cmds.select(selected, replace=True)
        cmds.sets(edit=True, forceElement=shading_group)
except Exception as e:
    print(f'[ProRigs] Error: {e}')