import logging, os, re, shutil
from pathlib import Path

from utils.logger import AppLogger
from views.import_scene_dialog import ImportSceneDialog

class ImportSceneController():
    def __init__(self, view: ImportSceneDialog, logger: AppLogger):
        super().__init__()
        self.view = view
        self.logger = logger

        self.view.imported_scene_file.connect(self.handle_imported_scene) # signal

    def handle_imported_scene(self, asset_type, scene_file):
        file_name = os.path.basename(scene_file)
        scene_name_pattern = r"^ProRigs_(.+)_v\d{2}\.\d{3}\.\d{3}\.(?:ma|mb)$"
        match = re.match(scene_name_pattern, file_name)
        
        if match:
            tgt_directory = Path(os.getenv('PRG_MAYA_SCENES')) / asset_type
            if not os.path.exists(tgt_directory):
                os.makedirs(tgt_directory)
                self.logger.log(f"Created directory: {tgt_directory}")

            # TODO: verify that a scene file of same asset doesn't exist
            # TODO: verify file isn't already there
            try:
                shutil.move(scene_file, tgt_directory)
                self.logger.log(f'Success "{file_name}", imported to: {tgt_directory}')
            except Exception as e:
                self.logger.log(f'Failed to import "{file_name}": {str(e)}', logging.ERROR)
        else:
            self.logger.log(f'Failed to import. Scene file name invalid: {file_name}', logging.ERROR)

