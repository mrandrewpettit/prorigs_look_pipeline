import os

from pathlib import Path

class RenderScene():
    def __init__(self):
        self.render_dir = Path(os.getenv('PRG_ASSETS')) / 'dev' / 'rigs' / os.getenv('PR_ASSET_TYPE') / os.getenv('PR_ASSET_NAME') / 'render'
        self.render_scene_name = os.getenv('PR_ASSET_NAME') + '.ma'

    def open(self):
        render_scene_file