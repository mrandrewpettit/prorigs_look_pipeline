from PySide2.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from tools.src.prorigs.old.assets_view import AssetsView
from tools.src.prorigs.old.assets_controller import AssetsController
from tools.src.prorigs.old.assets_model import AssetsModel

class OpenFileView(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.logger = logger.get_logger()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle('Open')

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        self.assets_model = AssetsModel()
        self.assets_view = AssetsView()
        self.assets_controller = AssetsController(self.assets_model, self.assets_view)

        self.open_button = QPushButton('Open Scene File')

        main_layout.addWidget(self.assets_view)
        main_layout.addWidget(self.open_button)

        self.setCentralWidget(central_widget)