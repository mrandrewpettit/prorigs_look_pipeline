import logging, os, subprocess

from models.launcher_model import LauncherModel
from utils.logger import AppLogger
#from controllers.import_scene_controller import ImportSceneController
#from controllers.new_asset_controller import NewAssetController
#from views.import_scene_dialog import ImportSceneDialog
from views.list_selection_dialog import ListSelectionDialog
#from views.new_asset_dialog import NewAssetDialog
from views.launcher_view import LauncherView

class LauncherController():
    def __init__(self, view: LauncherView, model: LauncherModel, logger: AppLogger):
        self.model = model
        self.view = view
        self.logger = logger

        self._init_view_data()

        self.view.softwares_combo_box.currentIndexChanged.connect(self._update_software)
        self.view.software_versions_combo_box.currentIndexChanged.connect(self._update_software_version)

        self.view.launch_button.clicked.connect(self.open_software)
        #self.view.import_scene_file_button.clicked.connect(self.import_scene_file)
        #self.view.package_button.clicked.connect(self.package)

        self.logger.log('Initialized ProRigs Dashboard', logging.INFO)

    def _init_view_data(self):
        softwares = self.model.get_softwares()
        self.view.update_softwares(softwares)

        software_versions = self.model.get_software_versions()
        self.view.update_software_versions(software_versions)

    def _update_software_version(self):
        new_software_version = self.view.software_versions_combo_box.currentText()
        self.model.set_current_software_version(new_software_version)

    def _update_software(self):
        new_software = self.view.softwares_combo_box.currentText()
        self.model.set_current_software(new_software)

        self.model.update_software_versions()
        software_versions = self.model.get_software_versions()
        self.view.update_software_versions(software_versions)

    '''
    def create_new_asset(self):
        new_asset_dialog = NewAssetDialog(self.view)
        NewAssetController(new_asset_dialog, self.logger)
        new_asset_dialog.exec()
        
        self.view.assets_controller.load_asset_names()
    
    def import_scene_file(self):
        import_scene_dialog = ImportSceneDialog(self.view)
        ImportSceneController(self.import_scene_dialog, self.logger)
        import_scene_dialog.exec()
    '''
    def open_software(self):
        def init_env(env):
            for env_var in env:
                os.environ[env_var] = env[env_var]

        tgt_software = self.model.get_current_software()

        env = {}
        exe = ''
        if tgt_software == 'maya':
            env = self.model.get_maya_env()
            init_env(env)
            exe = os.environ['MAYA_EXE']
        elif tgt_software == 'substance painter':
            env = self.model.get_substance_painter_env()
            init_env(env)
            exe = os.environ['SUBSTANCE_PAINTER_EXE']
        elif tgt_software == 'houdini':
            env = self.model.get_houdini_env()
            init_env(env)
            exe = os.environ['HOUDINI_EXE']
        else:
            print(f'ERROR: selected software ("{tgt_software}") not recognized')

        try:
            if not exe:
                raise EnvironmentError('exe environment variable is not set.')
            if not os.path.exists(exe):
                raise FileNotFoundError(f'Maya executable not found at: {exe}')

            process = subprocess.Popen([exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process  # Return the process to capture output (Stdout and Stderr)

        except (EnvironmentError, FileNotFoundError) as e:
            print(f'Error: {e}')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')

    def _open_maya(self):
        # set maya env vars
        maya_env = self.model.get_maya_env()
        for env_var in maya_env:
            os.environ[env_var] = maya_env[env_var]

        try:
            maya_exe = os.environ.get('MAYA_EXE')
            if not maya_exe:
                raise EnvironmentError('MAYA_EXE environment variable is not set.')
            if not os.path.exists(maya_exe):
                raise FileNotFoundError(f'Maya executable not found at: {maya_exe}')

            process = subprocess.Popen([maya_exe], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return process  # Return the process to capture output (Stdout and Stderr)

        except (EnvironmentError, FileNotFoundError) as e:
            print(f'Error: {e}')
        except Exception as e:
            print(f'An unexpected error occurred: {e}')

    def _open_substance_painter(self):
        substance_painter_env = self.model.get_substance_painter_env()
        for env_var in substance_painter_env:
            os.environ[env_var] = substance_painter_env[env_var]

        test = os.environ['SUBSTANCE_PAINTER_EXE']
        print(f'SUB PAINTER EXE: {test}')
        
        
"""
    def package(self):
        # set Geo Reference: Normal
		# vis NURBs curves & NURBs surfaces
		# disable film/res gate in viewport
		# set ProRigs attribute
		# are all texture files realtive to sourceimage
		# any unassigned shadgingroups
		# set Geo COmplexity: 1
		# set arnold subdiv type attrib
		# set arnold subdiv iteration
		# don't package tex files that aren't referenced in the maya scene

        asset_name = self.view.asset_names_combo_box.currentText()
        try:
            asset_scene_files = utils.get_asset_scene_files(asset_name)
            print(f'ASSET SCENE FILES: {asset_scene_files}')
        except FileExistsError or FileNotFoundError as e:
            pass # TODO: print error message to log

        # TODO: finish this functionality
"""