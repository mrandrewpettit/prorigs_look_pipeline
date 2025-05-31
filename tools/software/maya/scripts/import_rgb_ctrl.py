import os
from pathlib import Path

import maya.cmds as cmds

def import_rgb_ctrl():
    rgb_ctrl_file = Path(os.environ['PRG_MAYA']) / 'templates' / 'rgb_color_system_v02.00.ma'
    cmds.file(rgb_ctrl_file, i=True, rpr="rgb_color_system_v02_00")

if __name__ == "__main__":
    import_rgb_ctrl()