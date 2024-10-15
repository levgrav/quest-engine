from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QComboBox,
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt
import ctypes
import sys
from view.page import Page


class MainMenuPage(Page):
    def __init__(self, view_model, parent: QMainWindow, stacked_widget: QStackedWidget):
        super().__init__(
            view_model=view_model,
            parent=parent,
            stacked_widget=stacked_widget,
            page_name="main_menu",
        )
        self.setObjectName("main_menu")
        self.background_image_path = "files/cinematic_wallpapers/play_book_scenes.webp"

    def init_ui(self):
        """Initialize the main menu layout."""
        menu_layout = QVBoxLayout(self)

        # Create dark overlay with icon and title
        overlay = self.create_overlay()
        menu_layout.addWidget(overlay, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create buttons (Play, Settings, Donate, Quit)
        play_button = self.create_button(
            "Play", width=545, callback=lambda: self.view_model.show_page("game_select"), object_name="main_menu_button"
        )
        settings_button = self.create_button("Settings", 265, object_name="main_menu_button")
        donate_button = self.create_button("Donate", 265, object_name="main_menu_button")
        quit_button = self.create_button("Quit Game", 545, callback=QApplication.quit, object_name="main_menu_button")
        
        # Add buttons to layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(settings_button)
        button_layout.addWidget(donate_button)

        menu_layout.addWidget(play_button, alignment=Qt.AlignmentFlag.AlignHCenter)
        menu_layout.addLayout(button_layout)
        menu_layout.setAlignment(button_layout, Qt.AlignmentFlag.AlignHCenter)
        menu_layout.addWidget(quit_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        menu_layout.setContentsMargins(50, 50, 50, 50)
        menu_layout.setSpacing(15)

    def create_overlay(self):
        """Create the dark overlay with icon and title."""
        overlay = QWidget(self)
        overlay.setObjectName("overlay")
        overlay_layout = QHBoxLayout(overlay)
        overlay_layout.setContentsMargins(30, 20, 30, 20)

        # Icon (Q)
        icon_label = QLabel(self)
        pixmap = QPixmap("files/icon/icon_transparent.svg").scaled(
            120, 120, Qt.AspectRatioMode.KeepAspectRatio
        )
        icon_label.setPixmap(pixmap)
        overlay_layout.addWidget(icon_label)

        # Title ("uest Engine")
        title_label = QLabel("uest Engine")
        title_label.setObjectName("title")
        overlay_layout.addWidget(title_label)

        return overlay
