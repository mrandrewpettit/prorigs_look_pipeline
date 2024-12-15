from pathlib import Path
import os,sys

from dotenv import load_dotenv
from PySide2.QtWidgets import QApplication
from qt_material import apply_stylesheet

from utils.logger import AppLogger
from controllers.launcher_controller import LauncherController
from models.launcher_model import LauncherModel
from views.launcher_view import LauncherView

if __name__ == '__main__':
	# TODO: dotenv is temp, and eventaully want to set env var in the prorigs launcher bat file
	    # and will remove python-dotenv, remove module import, and .env file
    env_path = Path(__file__).resolve().parent / 'tools' / '.env'
    load_dotenv(env_path)

    app = QApplication(sys.argv)
    
    apply_stylesheet(app, theme='dark_amber.xml')

    logger = AppLogger('logs/app.log')
    
    view = LauncherView(logger)
    #logger.add_text_handler(view.log_text_edit)
    model = LauncherModel()
    controller = LauncherController(view, model, logger)

    view.show()
    sys.exit(app.exec_())