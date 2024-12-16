from models.assets_model import AssetsModel
from views.assets_widget import AssetsWidget

class AssetsController:
    def __init__(self, model: AssetsModel, view: AssetsWidget):
        self.model = model
        self.view = view

        self._init_view_data()

        self.view.asset_types_combo_box.currentIndexChanged.connect(self._update_asset_type)
        self.view.asset_names_combo_box.currentIndexChanged.connect(self._update_asset_name)

    def _update_asset_name(self):
        new_asset_name = self.view.asset_names_combo_box.currentText()
        self.model.set_current_asset_name(new_asset_name)

    def _update_asset_type(self):
        new_asset_type = self.view.asset_types_combo_box.currentText()
        self.model.set_current_asset_type(new_asset_type)

        self.model.update_asset_names()
        asset_names = self.model.get_asset_names()
        self.view.update_asset_names(asset_names)

    def _init_view_data(self):
        asset_types = self.model.get_asset_types()
        self.view.update_asset_types(asset_types)

        asset_names = self.model.get_asset_names()
        self.view.update_asset_names(asset_names)