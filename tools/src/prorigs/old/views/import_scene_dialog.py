#TODO might be able to craete a parent dialog that uses a buttonbox

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout

from tools.lib.controllers.assets_controller import AssetsController
from tools.lib.models.assets_model import AssetsModel
from tools.lib.views.assets_view import AssetsView

class ImportSceneDialog(QDialog):
    imported_scene_file = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Import a Scene File")

        self.main_layout = QVBoxLayout(self)

        self.browse_layout = QHBoxLayout(self)

        self.file_path_line_edit = QLineEdit(self)
        self.file_path_line_edit.setReadOnly(True)
        self.file_path_line_edit.setPlaceholderText("Select a Maya scene file...") 
        self.browse_button = QPushButton("Browse", self)

        self.browse_layout.addWidget(self.file_path_line_edit)
        self.browse_layout.addWidget(self.browse_button)

        self.assets_model = AssetsModel()
        self.assets_view = AssetsView()
        self.assets_controller = AssetsController(self.assets_model, self.assets_view)
        self.assets_view.asset_names_label.hide()
        self.assets_view.asset_names_combo_box.hide()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        self.main_layout.addLayout(self.browse_layout)
        self.main_layout.addWidget(self.assets_view)
        self.main_layout.addWidget(self.button_box)

        # TODO: add below to new controller (including methods probably, except update_accept_button)
        self.browse_button.clicked.connect(self.browse_file)

        self.button_box.accepted.connect(self.on_ok_clicked)
        self.button_box.rejected.connect(self.reject)
        self.browse_button.clicked.connect(self.update_accept_button)

    def update_accept_button(self):
        is_valid = self.file_path_line_edit.text() is not ''
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(is_valid)

    def on_ok_clicked(self):
        scene_file = self.file_path_line_edit.text().strip()
        asset_type = self.assets_view.asset_types_combo_box.currentText()
        self.imported_scene_file.emit(asset_type, scene_file)  # Emit signal to controller
        self.accept()

    def browse_file(self):
        # Open a file dialog to select a file
        options = QFileDialog.Options()
        selected_file, _ = QFileDialog.getOpenFileName(self, "Select a Maya Scene File", "", "Maya ASCII Files (*.ma);;All Files (*)", options=options)
        if selected_file:
            # Set the selected file path in the text field
            self.file_path_line_edit.setText(selected_file)