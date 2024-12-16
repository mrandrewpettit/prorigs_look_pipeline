from pathlib import Path
import sys

from PySide2.QtWidgets import QApplication
from qt_material import apply_stylesheet

from utils.logger import AppLogger
from controllers.launcher_controller import LauncherController
from models.launcher_model import LauncherModel
from views.launcher_mainWindow import LauncherMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    apply_stylesheet(app, theme='dark_amber.xml')

    logger = AppLogger('logs/app.log')
    
    view = LauncherMainWindow(logger)
    #logger.add_text_handler(view.log_text_edit)
    model = LauncherModel()
    controller = LauncherController(view, model, logger)

    view.show()
    sys.exit(app.exec_())