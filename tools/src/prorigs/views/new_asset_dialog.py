#TODO might be able to craete a parent dialog that uses a buttonbox

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QVBoxLayout

from views.assets_widget import AssetsWidget
from controllers.assets_controller import AssetsController
from models.assets_model import AssetsModel

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
        self.assets_widget = AssetsWidget()
        self.assets_controller = AssetsController(self.assets_model, self.assets_widget)
        self.assets_widget.toggle_asset_names(False)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addWidget(self.assets_widget)
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
        asset_type = self.assets_widget.asset_types_combo_box.currentText()
        print(f"Emitting signal: asset_type={asset_type}, asset_name={asset_name}")  # Debugging line
        self.new_asset.emit(asset_type, asset_name)  # Emit signal to controller
        self.accept()  # Close the dialog