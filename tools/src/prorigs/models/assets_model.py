import os
from pathlib import Path

class AssetsModel:
    def __init__(self):
        self._rig_dir = Path(os.getenv("PRG_ASSETS")) / 'dev' / 'rigs'

        self._asset_types = [
            item for item in os.listdir(self._rig_dir)
            if (self._rig_dir / item).is_dir()
        ]
        self._curr_asset_type = self._asset_types[0]
        
        self.update_asset_names()
    '''
    def get_asset_files(self):
        type_dir = Path(os.getenv('PRG_MAYA_SCENES')) / self._curr_asset_type

        asset_files = []
        for file in os.listdir(type_dir):
            file_path = os.path.join(type_dir, file)
            if os.path.isfile(file_path) and self._curr_asset_name.lower() in file.lower():
                asset_files.append(file_path)

        return asset_files
    '''
    def get_asset_names(self):
        return self._asset_names

    def get_asset_types(self):
        return self._asset_types

    def get_current_asset_type(self):
        return self._curr_asset_type
    
    def get_current_asset_name(self):
        return self._curr_asset_name

    def set_current_asset_type(self, type):
        self._curr_asset_type = type

    def set_current_asset_name(self, asset):
        self._curr_asset_name = asset

    def update_asset_names(self):
        asset_type_dir = Path(self._rig_dir) / self._curr_asset_type
        self._asset_names = [
            item for item in os.listdir(asset_type_dir)
            if (asset_type_dir / item).is_dir()
        ]

        self._curr_asset_name = self._asset_names[0]