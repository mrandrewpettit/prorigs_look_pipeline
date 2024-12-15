import random

def get_rand_color():
    r = random.uniform(0, 1)
    g = random.uniform(0, 1)
    b = random.uniform(0, 1)
    return (r, g, b)
    
def add_material(obj_name, mat_name):
    # TODO: check if material already exists
    
    # TODO: check if tab already exists, if it does pritn warngin
    cmds.nodeEditor("hyperShadePrimaryNodeEditor", e=True, createTab=[-1, mat_name])

    cmds.addAttr(obj_name, longName=mat_name+'Shader', attributeType='enum', enumName='Original=0:Custom=1', keyable=True)
    cmds.addAttr(obj_name, longName=mat_name+'Red', niceName = 'Red', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)
    cmds.addAttr(obj_name, longName=mat_name+'Green', niceName = 'Green', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)
    cmds.addAttr(obj_name, longName=mat_name+'Blue', niceName = 'Blue', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)        
    cmds.addAttr(obj_name, longName=mat_name+'Exposure', niceName = 'Exposure', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)
        
    aiStandardSurface = cmds.shadingNode('aiStandardSurface', name=f'ai_{mat_name}', asShader=True)
    blinn = cmds.shadingNode('blinn', name=f'b_{mat_name}', asShader=True)
    shadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'sg_{mat_name}')
    placeTex = cmds.shadingNode('place2dTexture', name=f'p2t_{mat_name}', asUtility=True)
    baseColor_file = cmds.shadingNode('file', name=f'f_{mat_name}_baseColor', isColorManaged=True, asTexture=True)
    blendInv_floatMath = cmds.shadingNode('floatMath', name=f'fm_{mat_name}_blendInv', asUtility=True)
    black_blend = cmds.shadingNode('blendColors', name=f'bc_{mat_name}_black', asUtility=True)
    white_blend = cmds.shadingNode('blendColors', name=f'bc_{mat_name}_white', asUtility=True)
    xpos_condition = cmds.shadingNode('condition', name=f'c_{mat_name}_xpos', asUtility=True)
    rgb_colorMath = cmds.shadingNode('colorMath', name=f'cm_{mat_name}_rgb', asUtility=True)
    clamp = cmds.shadingNode('colorCorrect', name=f'cc_{mat_name}_clamp', asUtility=True)
    rgb_blend = cmds.shadingNode('blendColors', name=f'bc_{mat_name}_rgb', asUtility=True)
        
    randColor = get_rand_color()
    cmds.setAttr(f'{baseColor_file}.defaultColor', randColor[0], randColor[1], randColor[2], type='float3')
    cmds.setAttr(f'{blendInv_floatMath}.floatB', -1.0)
    cmds.setAttr(f'{blendInv_floatMath}.operation', 2)
    cmds.setAttr(f'{black_blend}.color1', 0, 0, 0)
    cmds.setAttr(f'{white_blend}.color1', 1, 1, 1)
    cmds.setAttr(f'{xpos_condition}.operation', 3)
    cmds.setAttr(f'{clamp}.colClamp', 1)
    cmds.setAttr(f'{blinn}.diffuse', 1.0)
    cmds.setAttr(f'{blinn}.specularRollOff', 1.0)
    cmds.setAttr(f'{blinn}.reflectivity', 0.0)
        
    ctrl_name = 'RGBbrush_ctrl'
    cmds.connectAttr(f'{placeTex}.coverage', f'{baseColor_file}.coverage')
    cmds.connectAttr(f'{placeTex}.translateFrame', f'{baseColor_file}.translateFrame')
    cmds.connectAttr(f'{placeTex}.rotateFrame', f'{baseColor_file}.rotateFrame')
    cmds.connectAttr(f'{placeTex}.mirrorU', f'{baseColor_file}.mirrorU')
    cmds.connectAttr(f'{placeTex}.mirrorV', f'{baseColor_file}.mirrorV')
    cmds.connectAttr(f'{placeTex}.stagger', f'{baseColor_file}.stagger')
    cmds.connectAttr(f'{placeTex}.wrapU', f'{baseColor_file}.wrapU')
    cmds.connectAttr(f'{placeTex}.wrapV', f'{baseColor_file}.wrapV')
    cmds.connectAttr(f'{placeTex}.repeatUV', f'{baseColor_file}.repeatUV')
    cmds.connectAttr(f'{placeTex}.offset', f'{baseColor_file}.offset')
    cmds.connectAttr(f'{placeTex}.rotateUV', f'{baseColor_file}.rotateUV')
    cmds.connectAttr(f'{placeTex}.noiseUV', f'{baseColor_file}.noiseUV')
    cmds.connectAttr(f'{placeTex}.vertexUvOne', f'{baseColor_file}.vertexUvOne')
    cmds.connectAttr(f'{placeTex}.vertexUvTwo', f'{baseColor_file}.vertexUvTwo')
    cmds.connectAttr(f'{placeTex}.vertexUvThree', f'{baseColor_file}.vertexUvThree')
    cmds.connectAttr(f'{placeTex}.vertexCameraOne', f'{baseColor_file}.vertexCameraOne')
    cmds.connectAttr(f'{placeTex}.outUV', f'{baseColor_file}.uv')
    cmds.connectAttr(f'{placeTex}.outUvFilterSize', f'{baseColor_file}.uvFilterSize')
    cmds.connectAttr(f'{baseColor_file}.outColor', f'{rgb_colorMath}.colorA')
    cmds.connectAttr(f'{baseColor_file}.outColor', f'{rgb_blend}.color2')
    cmds.connectAttr(f'{rgb_colorMath}.outColor', f'{clamp}.inColor')
    cmds.connectAttr(f'{clamp}.outColor', f'{black_blend}.color2')
    cmds.connectAttr(f'{clamp}.outColor', f'{white_blend}.color2')
    cmds.connectAttr(f'{blendInv_floatMath}.outFloat', f'{black_blend}.blender')        
    cmds.connectAttr(f'{black_blend}.output', f'{xpos_condition}.colorIfFalse')
    cmds.connectAttr(f'{white_blend}.output', f'{xpos_condition}.colorIfTrue')
    cmds.connectAttr(f'{xpos_condition}.outColor', f'{rgb_blend}.color1')
    cmds.connectAttr(f'{rgb_blend}.output', f'{aiStandardSurface}.baseColor')
    cmds.connectAttr(f'{rgb_blend}.output', f'{blinn}.color')
    cmds.connectAttr(f'{aiStandardSurface}.outColor', f'{shadingGroup}.aiSurfaceShader')
    cmds.connectAttr(f'{blinn}.outColor', f'{shadingGroup}.surfaceShader')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Shader', f'{rgb_blend}.blender')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Exposure', f'{blendInv_floatMath}.floatA')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Exposure', f'{white_blend}.blender')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Exposure', f'{xpos_condition}.firstTerm')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Red', f'{rgb_colorMath}.colorBR')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Green', f'{rgb_colorMath}.colorBG')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Blue', f'{rgb_colorMath}.colorBB')
        
    print(f'[ProRigs] Successfully added "{mat_name}" material RGB control attributes and shading nodes')
    cmds.confirmDialog(title='ProRigs', message=f'Successfully added "{mat_name}" layer', button=["OK"]) # TODO: dynamically add title
    
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
    # TODO: ask for custom settings for  a material. i.e. metals, skin, SSS objects, tongue, teeth, eyes

    if result == "OK":
        mat_name = cmds.promptDialog(query=True, text=True)
   
        selected = cmds.ls(selection=True) # TODO: use type to make sure object is selected (i.e. type='transform')
        # TODO: check for selection and if none ask if user wants to still proceed
        
        shading_group = add_material('RGBbrush_ctrl', mat_name)

        cmds.select(selected, replace=True)
        cmds.sets(edit=True, forceElement=shading_group)
except Exception as e:
    print(f'[ProRigs] Error: {e}')