import logging, os, shutil

from pathlib import Path

from utils.logger import AppLogger
from models.new_asset_model import NewAssetModel
from views.new_asset_dialog import NewAssetDialog

class NewAssetController():
    def __init__(self, view: NewAssetDialog, model: NewAssetModel, logger: AppLogger):
        super().__init__()
        self.view = view
        self.model = model
        self.logger = logger

        self.view.new_asset.connect(self._handle_new_asset) # signal

    def _handle_new_asset(self, asset_type, asset_name):
        # TODO: check for no white spaces
        asset_name = asset_name[0].lower() + asset_name[1:] #lowercase only first letter
        new_asset_directory = Path(os.getenv("PRG_ASSETS")) / 'dev' / 'rigs' / asset_type / asset_name
        if not os.path.exists(new_asset_directory):
            Path(new_asset_directory).mkdir()
            self._copy_workspace_file(new_asset_directory)
            self._create_asset_dirs(new_asset_directory)
            self.logger.log(f'Created "{asset_name}" of type "{asset_type}": {new_asset_directory}', logging.INFO)
        else:
            pass
            self.logger.log(f'Failed to create "{asset_name}" of type "{asset_type}". Already exists', logging.ERROR)

    def _copy_workspace_file(self, root_dir):
        source_file = self.model.get_maya_workspace_file()
        destination = Path(root_dir) / "workspace.mel"
        shutil.copy(source_file, destination)

    def _create_asset_dirs(self, root_dir):
        asset_dirs = self.model.get_asset_dirs()
        for folder in asset_dirs:
            folder_path = os.path.join(root_dir, folder)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)
                print(f"Directory created: {folder_path}")
            else:
                print(f"Directory already exists: {folder_path}")