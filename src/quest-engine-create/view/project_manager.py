import json
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QToolBar,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QTextEdit,
    QSplitter,
    QHBoxLayout,
    QToolBox,
    QFormLayout,
    QCheckBox,
    QSpinBox,
    QPushButton,
    QColorDialog,
    QLineEdit,
    QListWidget,
)
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from PyQt6.QtCore import Qt
import os


class ProjectManager:
    def __init__(self, main_window, ui_manager):
        self.main_window = main_window
        self.ui_manager = ui_manager

    def open_project(self, tree_item = None):
        # Prompt the user to select a project

        if not isinstance(tree_item, QTreeWidgetItem):
            project_name = self.ui_manager.text_prompt(
                "Open Project", "Enter project name:"
            )
        else:
            project_name = tree_item.text(0)
            
        self.main_window.view_model.open_project(project_name)

    def close_project(self):
        self.main_window.view_model.close_project()

    def create_project(self):
        # Prompt the user to enter a project name
        project_name = self.ui_manager.text_prompt(
            "Create Project", "Enter project name:"
        )
        # Example: Create a project named "My Project"
        self.main_window.view_model.create_project(project_name)

    def on_project_opened(self):
        # Clear layout and show the project layout
        self.ui_manager.update_ui()

    def on_project_closed(self):
        # Clear layout and show the no-project layout
        self.ui_manager.update_ui()
