import os

import maya.cmds as cmds
import pymel.core as pm

from PySide2.QtWidgets import QDialog

import utils.maya_settings as ms
from views.open_file_view import OpenFileView
from views.list_selection_dialog import ListSelectionDialog

class OpenFileController():
    def __init__(self, view: OpenFileView):
        self.view = view

        self._tgt_file = ''

        print("Initializing OpenFileController")  # Debugging print
        print("Signal exists on open_button:", hasattr(self.view.open_button, "clicked"))
        self.view.open_button.clicked.connect(self._open_file)

    def _check_curr_file(self): # TODO: this can be moved to a utility module
        if cmds.file(query=True, modified=True):
            result = cmds.confirmDialog(
            title="Warning: Scene Not Saved",
            message="Save changes to scene?",
            button=["Save", "Don't Save", "Cancel"],
            defaultButton="Save",
            cancelButton="Cancel",
            dismissString="Cancel"
        )
            
            if result == "Save":
                # Save the current scene
                is_saved = self._save_scene_with_prompt()
                if is_saved:
                    cmds.file(save=True)
                    return True
                else:
                    return False
            elif result == "Don't Save":
                return True
            elif result == "Cancel":
                # Cancel the operation
                print("Operation canceled.")
                return False
        else:
            return True

    def _save_scene_with_prompt(self): # TODO: this can be moved to a utility module
        # Check if the scene has a name
        current_scene = cmds.file(query=True, sceneName=True)
        
        if not current_scene:
            # Open a file browser to get a save location
            file_path = cmds.fileDialog2(
                caption="Save Scene As",
                fileMode=0,  # 0 for file saving
                startingDirectory="",
                fileFilter="Maya Files (*.ma *.mb)"
            )
            
            if not file_path:
                print("Save operation canceled.")
                return False
            else:
                cmds.file(rename=file_path[0])
                return True

    def _open_file(self):
        self._find_file()

        # TODO: not sure if i should decouple and cmds/pm methods to maya scripts folder
        if self._tgt_file:
            try:
                is_safe = self._check_curr_file()
                if is_safe:
                    os.environ['PR_ASSET_NAME'] = self.view.assets_view.asset_names_combo_box.currentText()
                    os.environ['PR_ASSET_TYPE'] = self.view.assets_view.asset_types_combo_box.currentText()
                    self.view.close()

                    cmds.file(self._tgt_file, open=True, force=True)
                    pm.displayInfo(f'[ProRigs] Opened scene file: {self._tgt_file}')
                    ms.configure_render_settings()
                    ms.configure_render_settings()

            except Exception as e:
                pm.displayWarning(f'[ProRigs] Error occured while opening file: {e}')

    def _find_file(self):
        asset_files = self.view.assets_model.get_asset_files()

        if len(asset_files) == 0:
            print(f'No scene files found for "{self.view.assets_model.get_current_asset_name()}"')
            self._tgt_file = ''
        elif len(asset_files) == 1:
            self._tgt_file = asset_files[0]
        else:
            def _selection_to_tgt_file(maya_file):
                self._tgt_file = maya_file
            
            dialog = ListSelectionDialog(asset_files, self.view)
            dialog.selected_item.connect(_selection_to_tgt_file)

            if dialog.exec_() == QDialog.Rejected:
                print('SELECTION CANCELLED')
                self._tgt_file = ''