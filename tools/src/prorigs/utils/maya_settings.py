import os

import maya.cmds as cmds

def _set_renderer(renderer_name):
    cmds.setAttr('defaultRenderGlobals.currentRenderer', renderer_name, type='string')
    print(f"# [ProRigs] Renderer set to: {renderer_name}")

def _set_renderer_aspect(width, height):
    cmds.setAttr("defaultResolution.width", width)
    cmds.setAttr("defaultResolution.height", height)
    cmds.setAttr("defaultResolution.deviceAspectRatio", float(width) / height)
    print(f"# [ProRigs] Renderer image size set to {width}x{height}.")

def _set_active_aovs(tgt_aovs):
    for aov in tgt_aovs:
        aov_node = f'aiAOV_{aov}'
        if not cmds.objExists(aov_node):
            aov_node = cmds.createNode('aiAOV', name=aov)
            cmds.setAttr(f'{aov_node}.name', aov, type='string')
            
        aov_list = 'defaultArnoldRenderOptions.aovList'
        existing_connections = cmds.listConnections(aov_list, destination=True) or []
        if aov not in existing_connections:
            num_connections = len(existing_connections)
            cmds.connectAttr(f'{aov}.message', f'{aov_list}[{num_connections}]')
            print(f"# [ProRigs] AOV '{aov}' added to active list.")

def configure_render_settings():
    print("# [ProRigs] Configured render settings")

    if not cmds.pluginInfo('mtoa', query=True, loaded=True):
        cmds.loadPlugin('mtoa')
        print("# [ProRigs] Loaded Arnold plugin")

    # Query an Arnold-specific attribute to ensure nodes are created
    if not cmds.objExists('defaultArnoldRenderOptions'):
        cmds.createNode('aiOptions', name='defaultArnoldRenderOptions')
        print("# [ProRigs] Created defaultArnoldRenderOptions node.")

    _set_renderer('arnold')
    _set_renderer_aspect(1920, 1080)
    cmds.setAttr('defaultArnoldRenderOptions.AASamples', 24)
    cmds.setAttr('defaultArnoldRenderOptions.renderDevice', 1)

    tgt_aovs = ['ID', 'coat', 'diffuse', 'emission', 'sheen', 'specular', 'sss', 'transmission']
    _set_active_aovs(tgt_aovs)

def configure_scene_settings():
    print("# [ProRigs] Configured Scene settings")

    maya_project = os.getenv("MAYA_PROJECT")
    if maya_project:
        print(f"Setting Maya project to: {maya_project}")
        cmds.workspace(maya_project, openWorkspace=True)
    else:
        print(f"Warning: Maya project not set")
    cmds.setAttr('hardwareRenderingGlobals.transparencyAlgorithm', 1)