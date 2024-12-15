from PySide2.QtWidgets import QComboBox, QFormLayout, QLabel, QWidget
from PySide2.QtGui import QFontMetrics

class AssetsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QFormLayout()

        self.asset_types_combo_box = QComboBox()
        self.asset_types_combo_box.setFixedWidth(200) # TODO: make this dynamic
        self.main_layout.addRow('Asset Type: ', self.asset_types_combo_box)

        self.asset_names_combo_box = QComboBox()
        self.asset_names_combo_box.setFixedWidth(200) # TODO: make this dynamic
        self.main_layout.addRow('Asset Name: ', self.asset_names_combo_box)

        self.setLayout(self.main_layout)

    def update_asset_names(self, items):
        self.asset_names_combo_box.clear()
        self.asset_names_combo_box.addItems(items)
    
    def update_asset_types(self, items):
        self.asset_types_combo_box.clear()
        self.asset_types_combo_box.addItems(items)        