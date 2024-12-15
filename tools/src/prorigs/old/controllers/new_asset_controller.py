import logging, os

from pathlib import Path

from utils.logger import AppLogger
from views.new_asset_dialog import NewAssetDialog

class NewAssetController():
    def __init__(self, view: NewAssetDialog, logger: AppLogger):
        super().__init__()
        self.view = view
        self.logger = logger

        self.view.new_asset.connect(self.handle_new_asset) # signal

    def handle_new_asset(self, asset_type, asset_name):
        asset_name = asset_name[0].lower() + asset_name[1:]
        new_asset_directory = Path(os.getenv("PRORIGS_ASSETS")) / 'dev' / 'rigs' / asset_type / asset_name
        if not os.path.exists(new_asset_directory):
            Path(new_asset_directory).mkdir()
            self.logger.log(f'Created "{asset_name}" of type "{asset_type}": {new_asset_directory}', logging.INFO)
        else:
            pass
            self.logger.log(f'Failed to create "{asset_name}" of type "{asset_type}". Already exists', logging.ERROR)