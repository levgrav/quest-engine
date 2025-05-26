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
import sys
import ctypes
from view.json_components import QJsonWidget, QJsonUI, QJsonText, QJsonValue
from view.project_manager import ProjectManager
from view.ai_manager import AIManager
from view.ui_manager import UIManager


class MainWindow(QMainWindow):
    def __init__(self, view_model, **kwargs):
        super().__init__()

        self.view_model = view_model
        self.setWindowTitle("Quest Engine Create")

        self.setWindowIcon(QIcon(r"files\icon\icon.svg"))
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        self.setGeometry(100, 100, 1200, 800)  # Adjust size as needed

        self.ui_manager = UIManager(self)
        self.project_manager = ProjectManager(self, self.ui_manager)
        self.ai_manager = AIManager(self, self.ui_manager)
        self.connect_signals()

    def connect_signals(self):
        self.view_model.project_opened.connect(self.project_manager.on_project_opened)
        self.view_model.project_closed.connect(self.project_manager.on_project_closed)
        self.ui_manager.ai_text_input.returnPressed.connect(
            self.ai_manager.process_ai_command
        )
        self.view_model.ai_response_ready.connect(self.ai_manager.update_ai_output)
        self.ui_manager.open_action.triggered.connect(self.project_manager.open_project)
        self.ui_manager.close_action.triggered.connect(
            self.project_manager.close_project
        )
        self.ui_manager.create_action.triggered.connect(
            self.project_manager.create_project
        )
        self.ui_manager.project_tree_view.itemDoubleClicked.connect(
            lambda item:  self.project_manager.open_project(item) if not self.view_model.is_project_open() else None
        )