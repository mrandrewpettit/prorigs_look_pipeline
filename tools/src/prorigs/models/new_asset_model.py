import os
from pathlib import Path

class NewAssetModel:
    def __init__(self):
        self._asset_dirs = ['geom', 'maya', 'render', 'sourceimages']
        self._maya_workspace_file = Path(os.environ['PRG_MAYA']) / 'common' / 'templates' / 'workspace.mel'

    def get_asset_dirs(self):
        return self._asset_dirs
    
    def get_maya_workspace_file(self):
        return self._maya_workspace_file