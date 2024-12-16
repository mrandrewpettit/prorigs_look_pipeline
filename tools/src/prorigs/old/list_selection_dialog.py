import os

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton

class ListSelectionDialog(QDialog):
    selected_item = Signal(str)

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select an Item')

        layout = QVBoxLayout(self)

        self.items = items
        configured_items = []
        for item in items:
            if os.path.isfile(item):
                configured_items.append(os.path.basename(item))
            else:
                configured_items.append(item)

        self.list_widget = QListWidget()
        self.list_widget.addItems(configured_items)
        layout.addWidget(self.list_widget)

        self.accept_button = QPushButton("Accept")
        layout.addWidget(self.accept_button)
        self.accept_button.clicked.connect(self.emit_selected_item)

    def emit_selected_item(self):
        selected_indexes = self.list_widget.selectedIndexes()
        if selected_indexes:
            selected_index = selected_indexes[0].row()
            self.selected_item.emit(self.items[selected_index])
            self.accept()
        else:
            print('NO ITEM SELECTED. PLEASE SELECT AN ITEM')        