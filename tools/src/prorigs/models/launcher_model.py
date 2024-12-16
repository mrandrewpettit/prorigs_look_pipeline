import os
from pathlib import Path

class LauncherModel:
    def __init__(self):
        self._available_software = {
            'maya': ['2022'],
            'substance painter': ['2024'],
            'houdini': ['20.5.445']
        }

        self._softwares = list(self._available_software.keys())
        self._curr_software = self._softwares[0]

        self.update_software_versions()

    def get_softwares(self):
        return self._softwares

    def get_software_versions(self):
        return self._software_versions
    
    def get_current_software(self):
        return self._curr_software
    
    def get_current_software_version(self):
        return self._curr_software_version
    
    def set_current_software(self, software):
        self._curr_software = software

    def set_current_software_version(self, version):
        self._curr_software_version = version
    
    def update_software_versions(self):
        self._software_versions = self._available_software[self._curr_software]
        self._curr_software_version = self._software_versions[0]

    def get_houdini_env(self):
        houdini_root = os.environ['SIDEFX_ROOT'] + f'Houdini {self._curr_software_version}\\'
        houdini_env = {
            'HOUDINI_EXE': f'{houdini_root}bin\\houdini.exe'
        }

        return houdini_env

    def get_maya_env(self, asset_type, asset_name):
        maya_root = os.environ['AUTODESK_ROOT'] + f'\\maya{self._curr_software_version}\\'
        
        maya_env = {
            'MAYA_APP_DIR': os.environ['PRG_MAYA'],
            'MAYA_PLUG_IN_PATH': os.environ['PRG_MAYA'] + 'plug-ins\\;',
            'MAYA_PROJECT': os.environ['PRG_ASSETS'] + f'dev\\rigs\\{asset_type}\\{asset_name}\\;',
            'MAYA_SHELF_PATH': os.environ['PRG_MAYA'] + 'shelves\\;',
            'MAYA_NO_HOME': '1',
            'MAYA_NO_HOME_ICON': '1',
            'MAYA_DISABLE_CIP': '1',
            'MAYA_DISABLE_CER': '1',
            'MAYA_DISABLE_PLUGIN_SCENE_MODIFIED_WARNING': '1',
            'MAYA_EXE': f'{maya_root}bin\\maya.exe',
            'PRG_ASSET_TYPE': asset_type,
            'PRG_ASSET_NAME': asset_name
        }

        return maya_env
    
    def get_substance_painter_env(self):
        substance_painter_root = os.environ['SUBSTANCE_PAINTER_ROOT'] + f'Substance 3D Painter {self._curr_software_version}'
        substance_painter_env = {
            'SUBSTANCE_PAINTER_EXE': f'{substance_painter_root}Adobe Substance 3D Painter.exe'
        }

        return substance_painter_env