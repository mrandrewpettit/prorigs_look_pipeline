# open_file.py
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Qt

from views.open_file_view import OpenFileView
from controllers.open_file_controller import OpenFileController
from utils.logger import AppLogger  # Optional, for logging

class OpenFile:
    def __init__(self):
        self.open_file_view = None
        self.open_file_controller = None

    def _get_maya_main_window(self):
        maya_main_window = omui.MQtUtil.mainWindow()
        return wrapInstance(int(maya_main_window), QWidget)

    def run(self):
        """
        Run OpenFile within the current Maya session.
        """
        maya_main_window = self._get_maya_main_window()

        self.open_file_view = OpenFileView(parent=maya_main_window)
        self.open_file_view.resize(400, 150)
        self.open_file_view.setWindowFlags(Qt.Window)

        # Pass logger to the controller if needed
        self.open_file_controller = OpenFileController(self.open_file_view)

        try:
            self.open_file_view.show()
        except Exception as e:
            self.logger.error(f"Error displaying OpenFile view: {e}")
