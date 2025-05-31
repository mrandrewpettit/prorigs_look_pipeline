from functools import partial
import maya.cmds as cmds

#TODO: as script is verify hypershade is not open then run script
def create_rgb_attrs(ctrl_name, mat_name):
    cmds.addAttr(ctrl_name, longName=mat_name+'Shader', attributeType='enum', enumName='Original=0:Custom=1', keyable=True)
    cmds.addAttr(ctrl_name, longName=mat_name+'Red', niceName = 'Red', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)
    cmds.addAttr(ctrl_name, longName=mat_name+'Green', niceName = 'Green', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)
    cmds.addAttr(ctrl_name, longName=mat_name+'Blue', niceName = 'Blue', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)        
    cmds.addAttr(ctrl_name, longName=mat_name+'Exposure', niceName = 'Exposure', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)

def create_file_node(mat_name, type, place_tex):
    file_node = cmds.shadingNode('file', name=f'f_{mat_name}_{type}', isColorManaged=True, asTexture=True)


    cmds.connectAttr(f'{place_tex}.coverage', f'{file_node}.coverage')
    cmds.connectAttr(f'{place_tex}.translateFrame', f'{file_node}.translateFrame')
    cmds.connectAttr(f'{place_tex}.rotateFrame', f'{file_node}.rotateFrame')
    cmds.connectAttr(f'{place_tex}.mirrorU', f'{file_node}.mirrorU')
    cmds.connectAttr(f'{place_tex}.mirrorV', f'{file_node}.mirrorV')
    cmds.connectAttr(f'{place_tex}.stagger', f'{file_node}.stagger')
    cmds.connectAttr(f'{place_tex}.wrapU', f'{file_node}.wrapU')
    cmds.connectAttr(f'{place_tex}.wrapV', f'{file_node}.wrapV')
    cmds.connectAttr(f'{place_tex}.repeatUV', f'{file_node}.repeatUV')
    cmds.connectAttr(f'{place_tex}.offset', f'{file_node}.offset')
    cmds.connectAttr(f'{place_tex}.rotateUV', f'{file_node}.rotateUV')
    cmds.connectAttr(f'{place_tex}.noiseUV', f'{file_node}.noiseUV')
    cmds.connectAttr(f'{place_tex}.vertexUvOne', f'{file_node}.vertexUvOne')
    cmds.connectAttr(f'{place_tex}.vertexUvTwo', f'{file_node}.vertexUvTwo')
    cmds.connectAttr(f'{place_tex}.vertexUvThree', f'{file_node}.vertexUvThree')
    cmds.connectAttr(f'{place_tex}.vertexCameraOne', f'{file_node}.vertexCameraOne')
    cmds.connectAttr(f'{place_tex}.outUV', f'{file_node}.uv')
    cmds.connectAttr(f'{place_tex}.outUvFilterSize', f'{file_node}.uvFilterSize')

    return file_node

def create_surface_nodes(shading_group, mat_name):
    aiStandardSurface = cmds.shadingNode('aiStandardSurface', name=f'ai_{mat_name}', asShader=True)
    blinn = cmds.shadingNode('blinn', name=f'b_{mat_name}', asShader=True)

    cmds.setAttr(f'{blinn}.diffuse', 1.0)
    cmds.setAttr(f'{blinn}.specularColor', 1.0, 1.0, 1.0)
    cmds.setAttr(f'{blinn}.reflectivity', 0.0)
    
    cmds.connectAttr(f'{aiStandardSurface}.outColor', f'{shading_group}.aiSurfaceShader')
    cmds.connectAttr(f'{blinn}.outColor', f'{shading_group}.surfaceShader')

    return aiStandardSurface, blinn 

def baseColor_setup(mat_color, mat_name, ctrl_name, place_tex):
    baseColor_file = create_file_node(mat_name, 'baseColor', place_tex)

    blendInv_floatMath = cmds.shadingNode('floatMath', name=f'fm_{mat_name}_blendInv', asUtility=True)
    black_blend = cmds.shadingNode('blendColors', name=f'bc_{mat_name}_black', asUtility=True)
    white_blend = cmds.shadingNode('blendColors', name=f'bc_{mat_name}_white', asUtility=True)
    xpos_condition = cmds.shadingNode('condition', name=f'c_{mat_name}_xpos', asUtility=True)
    rgb_colorMath = cmds.shadingNode('colorMath', name=f'cm_{mat_name}_rgb', asUtility=True)
    clamp = cmds.shadingNode('colorCorrect', name=f'cc_{mat_name}_clamp', asUtility=True)
    rgb_blend = cmds.shadingNode('blendColors', name=f'bc_{mat_name}_rgb', asUtility=True)

    cmds.setAttr(f'{baseColor_file}.defaultColor', mat_color[0], mat_color[1], mat_color[2], type='float3')
    cmds.setAttr(f'{blendInv_floatMath}.floatB', -1.0)
    cmds.setAttr(f'{blendInv_floatMath}.operation', 2)
    cmds.setAttr(f'{black_blend}.color1', 0, 0, 0)
    cmds.setAttr(f'{white_blend}.color1', 1, 1, 1)
    cmds.setAttr(f'{xpos_condition}.operation', 3)
    cmds.setAttr(f'{clamp}.colClamp', 1)
    
    cmds.connectAttr(f'{baseColor_file}.outColor', f'{rgb_colorMath}.colorA')
    cmds.connectAttr(f'{baseColor_file}.outColor', f'{rgb_blend}.color2')
    cmds.connectAttr(f'{rgb_colorMath}.outColor', f'{clamp}.inColor')
    cmds.connectAttr(f'{clamp}.outColor', f'{black_blend}.color2')
    cmds.connectAttr(f'{clamp}.outColor', f'{white_blend}.color2')
    cmds.connectAttr(f'{blendInv_floatMath}.outFloat', f'{black_blend}.blender')        
    cmds.connectAttr(f'{black_blend}.output', f'{xpos_condition}.colorIfFalse')
    cmds.connectAttr(f'{white_blend}.output', f'{xpos_condition}.colorIfTrue')
    cmds.connectAttr(f'{xpos_condition}.outColor', f'{rgb_blend}.color1')

    cmds.connectAttr(f'{ctrl_name}.{mat_name}Shader', f'{rgb_blend}.blender')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Exposure', f'{blendInv_floatMath}.floatA')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Exposure', f'{white_blend}.blender')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Exposure', f'{xpos_condition}.firstTerm')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Red', f'{rgb_colorMath}.colorBR')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Green', f'{rgb_colorMath}.colorBG')
    cmds.connectAttr(f'{ctrl_name}.{mat_name}Blue', f'{rgb_colorMath}.colorBB')

    b_color_correct = cmds.shadingNode('colorCorrect', name=f'b_{mat_name}_baseColor', asUtility=True)
    
    cmds.setAttr(f'{b_color_correct}.valGain', 1.5)
    
    cmds.connectAttr(f'{rgb_blend}.output', f'{b_color_correct}.inColor')

    return rgb_blend, b_color_correct

def roughness_setup(mat_name, ctrl_name, place_tex):
    roughness_file = create_file_node(mat_name, 'roughness', place_tex)
    
    ai_roughness_range = cmds.shadingNode('aiRange', name=f'ai_{mat_name}_roughness', asUtility=True)
    b_roughness_range = cmds.shadingNode('remapValue', name=f'b_{mat_name}_roughness', asUtility=True)
    
    
    cmds.connectAttr(f'{roughness_file}.outColor', f'{ai_roughness_range}.input')
    cmds.connectAttr(f'{roughness_file}.outAlpha', f'{b_roughness_range}.inputValue')

    return ai_roughness_range, b_roughness_range
    
def bump_setup(mat_name, place_tex):
    bump_file = create_file_node(mat_name, 'height', place_tex)
    normal_file = create_file_node(mat_name, 'normal', place_tex)
    
    b_bump = cmds.shadingNode('bump2d', name=f'b_{mat_name}_normal', asUtility=True)
    ai_normal = cmds.shadingNode('aiNormalMap', name=f'ai_{mat_name}_normal', asUtility=True)
    displacement = cmds.shadingNode('displacementShader', name=f'ds_{mat_name}', asUtility=True)

    cmds.setAttr(f'{b_bump}.bumpInterp', 1)

    cmds.connectAttr(f'{normal_file}.outAlpha', f'{b_bump}.bumpValue')
    cmds.connectAttr(f'{normal_file}.outColor', f'{ai_normal}.input')
    cmds.connectAttr(f'{bump_file}.outColorR', f'{displacement}.displacement')

    return b_bump, ai_normal, displacement

def create_RGB_material(ctrl_name, shading_group, mat_type):
    materials = cmds.listConnections(shading_group + ".surfaceShader", source=True) or []

    if len(materials) > 1:
        print(f'[ProRigs] Error: Multiple materials connected to {shading_group}')
        return
    elif len(materials) == 0:
        print(f'[ProRigs] Error: No materials connected to {shading_group}')
        return
    
    mat_name = shading_group.split('_')[-1]
    mat_color = cmds.getAttr(materials[0] + ".color")[0]
    
    cmds.delete(materials[0])    
    # TODO: rename shading group to have 'sg_' prefix
    
    # TODO: check if tab already exists, if it does print warning
    cmds.nodeEditor("hyperShadePrimaryNodeEditor", e=True, createTab=[-1, mat_name])

    create_rgb_attrs(ctrl_name, mat_name)
    
    aiStandardSurface, blinn = create_surface_nodes(shading_group, mat_name)
    place_tex = cmds.shadingNode('place2dTexture', name=f'p2t_{mat_name}', asUtility=True)
    
    ai_baseColor, b_baseColor = baseColor_setup(mat_color, mat_name, ctrl_name, place_tex)
    cmds.connectAttr(f'{ai_baseColor}.output', f'{aiStandardSurface}.baseColor')
    cmds.connectAttr(f'{b_baseColor}.outColor', f'{blinn}.color')

    ai_roughness, b_roughness = roughness_setup(mat_name, ctrl_name, place_tex)
    cmds.connectAttr(f'{ai_roughness}.outColorR', f'{aiStandardSurface}.specularRoughness')
    cmds.connectAttr(f'{b_roughness}.outValue', f'{blinn}.eccentricity')

    # TODO: combine normal/bump maps in shader instead of in texture
    b_bump, ai_normal, displacement = bump_setup(mat_name, place_tex)
    cmds.connectAttr(f'{b_bump}.outNormal', f'{blinn}.normalCamera')
    cmds.connectAttr(f'{ai_normal}.outValue', f'{aiStandardSurface}.normalCamera')
    cmds.connectAttr(f'{displacement}.displacement', f'{shading_group}.displacementShader')

    # TODO: fix this
    #if mat_type.lower() == 'metal':
    #    metal = create_file_node(mat_name, 'metalness')
    #    cmds.connectAttr(f'{metal}.outAlpha', f'{aiStandardSurface}.metalness')
    #    cmds.connectAttr(f'{b_baseColor}.output', f'{blinn}.specularColor')
        
    print(f'[ProRigs] Successfully added "{mat_name}" material RGB control attributes and shading nodes')
    cmds.confirmDialog(title='ProRigs', message=f'Successfully added "{mat_name}" layer', button=["OK"]) # TODO: dynamically add title

####################################################################################################
#prompt dialog
####################################################################################################

def on_accept(*args):
    selected_radio = cmds.radioCollection(radio_group, query=True, select=True)
    mat_type = cmds.radioButton(selected_radio, query=True, label=True)
    cmds.deleteUI("ProRigs", window=True)

    create_RGB_material('RGBbrush_ctrl', args[0], mat_type)

    process_next_shading_group()

def on_cancel(*args):
    print("Canceled")
    cmds.deleteUI("ProRigs", window=True)

    process_next_shading_group()

def create_type_prompt_dialog(shading_group):
    if cmds.window("ProRigs", exists=True):
        cmds.deleteUI("ProRigs", window=True)

    cmds.window("ProRigs", title="Select Option", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label=f'Convert {shading_group.split("_")[-1]}', align='center', height=30)

    global radio_group
    radio_group = cmds.radioCollection()

    cmds.radioButton(label='Default', select=True)
    cmds.radioButton(label='Metal')
    cmds.radioButton(label='Skin')

    cmds.separator(height=10, style='none')

    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150))
    cmds.button(label="Accept", command=partial(on_accept, shading_group))
    cmds.button(label="Cancel", command=on_cancel)

    cmds.showWindow("ProRigs")

####################################################################################################
#create_type_prompt_dialog doesn't work with traditional for-loop so running custom queue setup (i.e. process_shading_groups, process_next_shading_group)
####################################################################################################

def get_shading_groups_from_selected():
    selected = cmds.ls(selection=True, long=True)
    if not selected:
        print("No objects selected.")
        return []

    shading_groups = set() # Use a set to avoid duplicates

    for obj in selected:
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        
        for shape in shapes:
            sgs = cmds.listConnections(shape, type='shadingEngine') or []
            shading_groups.update(sgs)

    return list(shading_groups)

def process_next_shading_group():
    if not shading_group_queue:
        print("[ProRigs] All shading groups processed.")
        return

    shading_group = shading_group_queue.pop(0)
    create_type_prompt_dialog(shading_group)

def process_shading_groups():
    global shading_group_queue
    shading_group_queue = get_shading_groups_from_selected()
    if not shading_group_queue:
        print("[ProRigs] No shading groups to process.")
        return

    process_next_shading_group()