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


class AIManager:
    def __init__(self, main_window, ui_manager):
        self.main_window = main_window
        self.ui_manager = ui_manager

    def process_ai_command(self):
        """Handle user input, send command to the View-Model, and update output."""
        command = self.ui_manager.ai_text_input.text()

        # Clear the input field after the command is submitted
        self.ui_manager.ai_text_input.clear()

        # Display the command in the output area
        self.update_ai_output(f">>> {command}")

        # Send the command to the View-Model for processing
        self.main_window.view_model.process_ai_command(command)

        # update the layout to show the new data
        self.ui_manager.update_ui()

    def update_ai_output(self, message):
        """Update the AI output text area with a new message."""
        self.ui_manager.ai_text_output.append(message)
