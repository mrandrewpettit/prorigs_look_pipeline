#TODO might be able to craete a parent dialog that uses a buttonbox

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout

from tools.lib.views.assets_view import AssetsView
from tools.lib.controllers.assets_controller import AssetsController
from tools.lib.models.assets_model import AssetsModel

class NewAssetDialog(QDialog):
    new_asset = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle('Create a New Asset')

        self.main_layout = QVBoxLayout()

        self.input_layout = QFormLayout()

        self.asset_name_input = QLineEdit()
        self.input_layout.addRow('New Asset Name: ', self.asset_name_input)

        self.assets_model = AssetsModel()
        self.assets_view = AssetsView()
        self.assets_controller = AssetsController(self.assets_model, self.assets_view)
        self.assets_view.asset_names_label.hide()
        self.assets_view.asset_names_combo_box.hide()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.assets_view)
        self.main_layout.addWidget(self.button_box)
        
        self.setLayout(self.main_layout)

        # TODO: this can probably be moved toa controller (including methods probably)
        self.button_box.accepted.connect(self.on_ok_clicked)
        self.button_box.rejected.connect(self.reject)
        self.asset_name_input.textChanged.connect(self.update_accept_button)

    def update_accept_button(self):
        is_valid = self.asset_name_input is not None
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(is_valid)

    def on_ok_clicked(self):
        asset_name = self.asset_name_input.text().strip()
        asset_type = self.assets_view.asset_types_combo_box.currentText()
        self.new_asset.emit(asset_type, asset_name)  # Emit signal to controller
        self.accept()  # Close the dialog