from functools import partial
import maya.cmds as cmds

def get_shading_groups_from_selected():
    selected = cmds.ls(selection=True, long=True)  # Get selected objects
    if not selected:
        print("No objects selected.")
        return []

    shading_groups = set()  # Use a set to avoid duplicates

    for obj in selected:
        # Get all shapes of the selected object (in case of groups)
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        
        for shape in shapes:
            # Find the shading groups (shading engines) attached to the shape
            sgs = cmds.listConnections(shape, type='shadingEngine') or []
            shading_groups.update(sgs)  # Add found shading groups to the set

    return list(shading_groups)

def create_rgb_attrs(ctrl_name, mat_name):
    cmds.addAttr(ctrl_name, longName=mat_name+'Shader', attributeType='enum', enumName='Original=0:Custom=1', keyable=True)
    cmds.addAttr(ctrl_name, longName=mat_name+'Red', niceName = 'Red', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)
    cmds.addAttr(ctrl_name, longName=mat_name+'Green', niceName = 'Green', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)
    cmds.addAttr(ctrl_name, longName=mat_name+'Blue', niceName = 'Blue', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)        
    cmds.addAttr(ctrl_name, longName=mat_name+'Exposure', niceName = 'Exposure', attributeType='float', keyable=True, minValue=-1.0, maxValue=1.0)

def create_surface_nodes(shading_group, mat_name):
    aiStandardSurface = cmds.shadingNode('aiStandardSurface', name=f'ai_{mat_name}', asShader=True)
    blinn = cmds.shadingNode('blinn', name=f'b_{mat_name}', asShader=True)

    cmds.setAttr(f'{blinn}.diffuse', 1.0)
    cmds.setAttr(f'{blinn}.specularColor', 1.0, 1.0, 1.0)
    cmds.setAttr(f'{blinn}.reflectivity', 0.0)
    
    cmds.connectAttr(f'{aiStandardSurface}.outColor', f'{shading_group}.aiSurfaceShader')
    cmds.connectAttr(f'{blinn}.outColor', f'{shading_group}.surfaceShader')

    return aiStandardSurface, blinn
    
def create_file_node(mat_name, type):
    placeTex = cmds.shadingNode('place2dTexture', name=f'p2t_{mat_name}', asUtility=True)
    file_node = cmds.shadingNode('file', name=f'f_{mat_name}_{type}', isColorManaged=True, asTexture=True)


    cmds.connectAttr(f'{placeTex}.coverage', f'{file_node}.coverage')
    cmds.connectAttr(f'{placeTex}.translateFrame', f'{file_node}.translateFrame')
    cmds.connectAttr(f'{placeTex}.rotateFrame', f'{file_node}.rotateFrame')
    cmds.connectAttr(f'{placeTex}.mirrorU', f'{file_node}.mirrorU')
    cmds.connectAttr(f'{placeTex}.mirrorV', f'{file_node}.mirrorV')
    cmds.connectAttr(f'{placeTex}.stagger', f'{file_node}.stagger')
    cmds.connectAttr(f'{placeTex}.wrapU', f'{file_node}.wrapU')
    cmds.connectAttr(f'{placeTex}.wrapV', f'{file_node}.wrapV')
    cmds.connectAttr(f'{placeTex}.repeatUV', f'{file_node}.repeatUV')
    cmds.connectAttr(f'{placeTex}.offset', f'{file_node}.offset')
    cmds.connectAttr(f'{placeTex}.rotateUV', f'{file_node}.rotateUV')
    cmds.connectAttr(f'{placeTex}.noiseUV', f'{file_node}.noiseUV')
    cmds.connectAttr(f'{placeTex}.vertexUvOne', f'{file_node}.vertexUvOne')
    cmds.connectAttr(f'{placeTex}.vertexUvTwo', f'{file_node}.vertexUvTwo')
    cmds.connectAttr(f'{placeTex}.vertexUvThree', f'{file_node}.vertexUvThree')
    cmds.connectAttr(f'{placeTex}.vertexCameraOne', f'{file_node}.vertexCameraOne')
    cmds.connectAttr(f'{placeTex}.outUV', f'{file_node}.uv')
    cmds.connectAttr(f'{placeTex}.outUvFilterSize', f'{file_node}.uvFilterSize')

    return file_node

def baseColor_setup(mat_color, mat_name, ctrl_name):
    baseColor_file = create_file_node(mat_name, 'baseColor')

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

    return rgb_blend
    
def bump_setup(mat_name):
    bump_file = create_file_node(mat_name, 'bump')
    
    b_bump2d = cmds.shadingNode('bump2d', name=f'b2d_{mat_name}_blinn', asUtility=True)
    ai_bump2d = cmds.shadingNode('aiBump2d', name=f'ab2d_{mat_name}_ai', asUtility=True)
    ai_normal = cmds.shadingNode('aiNormalMap', name=f'anm_{mat_name}_ai', asUtility=True)
    displacement = cmds.shadingNode('displacementShader', name=f'ds_{mat_name}', asUtility=True)

    cmds.connectAttr(f'{bump_file}.outAlpha', f'{b_bump2d}.bumpValue')
    cmds.connectAttr(f'{bump_file}.outAlpha', f'{ai_bump2d}.bumpMap')
    cmds.connectAttr(f'{ai_bump2d}.outValue', f'{ai_normal}.input')
    cmds.connectAttr(f'{bump_file}.outAlpha', f'{displacement}.displacement')

    return b_bump2d, ai_normal, displacement

def to_RGB_material(ctrl_name, shading_group, mat_type):
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
    # rename shading group to have 'sg_' prefix
    
    # TODO: check if tab already exists, if it does print warning
    cmds.nodeEditor("hyperShadePrimaryNodeEditor", e=True, createTab=[-1, mat_name])

    create_rgb_attrs(ctrl_name, mat_name)
    
    aiStandardSurface, blinn = create_surface_nodes(shading_group, mat_name)
    
    baseColor = baseColor_setup(mat_color, mat_name, ctrl_name)
    cmds.connectAttr(f'{baseColor}.output', f'{aiStandardSurface}.baseColor')
    cmds.connectAttr(f'{baseColor}.output', f'{blinn}.color')
    
    roughness = create_file_node(mat_name, 'roughness')
    cmds.connectAttr(f'{roughness}.outAlpha', f'{aiStandardSurface}.specularRoughness')
    cmds.connectAttr(f'{roughness}.outAlpha', f'{blinn}.eccentricity')
    
    b_bump, ai_bump, displacement = bump_setup(mat_name)
    cmds.connectAttr(f'{b_bump}.outNormal', f'{blinn}.normalCamera')
    cmds.connectAttr(f'{ai_bump}.outValue', f'{aiStandardSurface}.normalCamera')
    cmds.connectAttr(f'{displacement}.displacement', f'{shading_group}.displacementShader')

    if mat_type.lower() == 'metal':
        metal = create_file_node(mat_name, 'metalness')
        cmds.connectAttr(f'{metal}.outAlpha', f'{aiStandardSurface}.metalness')
        cmds.connectAttr(f'{baseColor}.output', f'{blinn}.specularColor')
        
    print(f'[ProRigs] Successfully added "{mat_name}" material RGB control attributes and shading nodes')
    cmds.confirmDialog(title='ProRigs', message=f'Successfully added "{mat_name}" layer', button=["OK"]) # TODO: dynamically add title

def on_selection_change(*args):
    """Callback function to handle radio button selection change."""
    selected_value = cmds.radioCollection(radio_group, query=True, select=True)
    print(f"Selected: {selected_value}")  # You can perform actions based on selection here

def create_type_prompt_dialog(shading_group):
    """Create a custom dialog with radio buttons."""
    if cmds.window("ProRigs", exists=True):
        cmds.deleteUI("ProRigs", window=True)

    cmds.window("ProRigs", title="Select Option", widthHeight=(300, 150))
    cmds.columnLayout(adjustableColumn=True)

    cmds.text(label=f'Convert {shading_group.split("_")[-1]}', align='center', height=30)

    # Create a radio collection for exclusive selection
    global radio_group
    radio_group = cmds.radioCollection()

    cmds.radioButton(label='Default', select=True)
    cmds.radioButton(label='Metal')
    cmds.radioButton(label='Skin')

    cmds.separator(height=10, style='none')

    # Add Accept and Cancel buttons
    cmds.rowLayout(numberOfColumns=2, columnWidth2=(150, 150))
    cmds.button(label="Accept", command=partial(on_accept, shading_group))
    cmds.button(label="Cancel", command=on_cancel)

    cmds.showWindow("ProRigs")

def on_accept(*args):
    """Handle Accept button click."""
    cmds.deleteUI("ProRigs", window=True)
    
    selected_radio = cmds.radioCollection(radio_group, query=True, select=True)
    mat_type = cmds.radioButton(selected_radio, query=True, label=True)
    to_RGB_material('RGBbrush_ctrl', shading_group, mat_type)

def on_cancel(*args):
    """Handle Cancel button click."""
    print("Canceled")
    cmds.deleteUI("ProRigs", window=True)

try:
    shading_groups = get_shading_groups_from_selected()
    shading_groups = sorted(shading_groups)
    
    for shading_group in shading_groups:
        # TODO: dynamically add title/message
        create_type_prompt_dialog(shading_group)
except Exception as e:
    print(f'[ProRigs] Error: {e}')

