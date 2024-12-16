import os, sys

import maya.cmds as cmds

def _import_prorigs_lib():
	prorigs_python_path = os.path.join(os.getenv('PRG_PYTHON_LIBS'), 'prorigs')
	if prorigs_python_path not in sys.path:
		sys.path.append(prorigs_python_path)

def Initialize():
	print("# [ProRigs] ProRigs Environment User Setup")

	_import_prorigs_lib()
	import utils.maya_settings as ms
	
	ms.configure_scene_settings()
	ms.configure_render_settings()

cmds.evalDeferred('Initialize()')