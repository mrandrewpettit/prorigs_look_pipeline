from PySide2.QtWidgets import QComboBox, QFormLayout, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSizePolicy, QSpacerItem, QTextEdit, QVBoxLayout, QWidget

from views.assets_widget import AssetsWidget
from controllers.assets_controller import AssetsController
from models.assets_model import AssetsModel

class LauncherMainWindow(QMainWindow):
    def __init__(self, logger, parent=None):
        super().__init__(parent)
        self.logger = logger.get_logger()
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle('ProRigs Launcher')

        central_widget = QWidget()
        main_layout = QFormLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.assets_model = AssetsModel()
        self.assets_widget = AssetsWidget()
        self.assets_controller = AssetsController(self.assets_model, self.assets_widget)

        self.softwares_combo_box = QComboBox()
        self.software_versions_combo_box = QComboBox()
        self.launch_button = QPushButton("Launch")

        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        #self.import_scene_file_button = QPushButton('Import Scene File')
        #self.package_button = QPushButton('Package')
        self.new_asset_button = QPushButton('New Asset')
        #spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        #self.log_text_edit = QTextEdit()
        #self.log_text_edit.setLineWrapMode(QTextEdit.NoWrap)
        #self.log_text_edit.setReadOnly(True)

        main_layout.addRow(self.assets_widget)
        main_layout.addRow("Software:", self.softwares_combo_box)
        main_layout.addRow("Version:", self.software_versions_combo_box)
        main_layout.addRow(self.launch_button)
        main_layout.addItem(spacer)
        #main_layout.addWidget(self.import_scene_file_button)
        #main_layout.addWidget(self.package_button)
        main_layout.addRow(self.new_asset_button)
        #main_layout.addRow(self.log_text_edit)

        self.setCentralWidget(central_widget)
    '''
    def update_asset_names(self, items):
        self.asset_names_combo_box.clear()
        self.asset_names_combo_box.addItems(items)
    
    def update_asset_types(self, items):
        self.asset_types_combo_box.clear()
        self.asset_types_combo_box.addItems(items)    
    '''
    def update_softwares(self, items):
        self.softwares_combo_box.clear()
        self.softwares_combo_box.addItems(items)
    
    def update_software_versions(self, items):
        self.software_versions_combo_box.clear()
        self.software_versions_combo_box.addItems(items)