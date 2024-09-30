# gui.py
from PyQt6.QtWidgets import (
    QMainWindow,
    QTextEdit,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QSplitter,
    QListWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from view.page import Page


class GamePage(Page):
    def __init__(self, view_model, parent, stacked_widget):
        super().__init__(view_model, parent, stacked_widget, "game")
        # self.background_image_path = (
        #     "files/cinematic_wallpapers/play_on_ariship_pose.webp"
        # )

    def init_ui(self):
        """Initialize the game window layout."""
        main_splitter = QSplitter()

        # Left Panel (Inventory)
        self.init_left_panel(main_splitter)

        # Center Panel (Game Text and Command Input)
        self.init_center_panel(main_splitter)

        # Right Panel (Player Status)
        self.init_right_panel(main_splitter)

        # Bottom Panel (Optional Quick Action Buttons)
        bottom_panel = self.init_bottom_panel()

        # Main layout
        layout = QVBoxLayout()
        layout.addWidget(main_splitter)
        layout.addWidget(bottom_panel)

        self.setLayout(layout)

    def init_left_panel(self, main_splitter):
        """Sets up the left panel (Inventory)."""
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        self.inventory_list = QListWidget()
        self.inventory_list.setFixedWidth(200)
        left_layout.addWidget(QLabel("Inventory"))
        left_layout.addWidget(self.inventory_list)

        main_splitter.addWidget(left_panel)

    def init_center_panel(self, main_splitter):
        """Sets up the center panel (Game Text and Command Input)."""
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)

        self.game_text_output = QTextEdit()
        self.game_text_output.setReadOnly(True)

        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter command...")

        center_layout.addWidget(self.game_text_output)
        center_layout.addWidget(self.command_input)

        main_splitter.addWidget(center_panel)

    def init_right_panel(self, main_splitter):
        """Sets up the right panel (Status and Stats)."""
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.location_label = QLabel("Location: Unknown")
        self.health_label = QLabel("Health: 100")

        right_layout.addWidget(QLabel("Player Status"))
        right_layout.addWidget(self.location_label)
        right_layout.addWidget(self.health_label)

        main_splitter.addWidget(right_panel)

    def init_bottom_panel(self):
        """Optional bottom panel with quick action buttons."""
        bottom_panel = QWidget()
        bottom_layout = QHBoxLayout(bottom_panel)

        look_button = QPushButton("Look")
        inventory_button = QPushButton("Inventory")
        help_button = QPushButton("Help")

        bottom_layout.addWidget(look_button)
        bottom_layout.addWidget(inventory_button)
        bottom_layout.addWidget(help_button)

        return bottom_panel

    def connect_signals(self):
        """Connect signals for user interaction."""
        self.command_input.returnPressed.connect(self.process_command)

    def process_command(self):
        """Handle the command input from the user."""
        command = self.command_input.text()

        self.command_input.clear()

        self.game_text_output.append(f">>> {command}")

        self.view_model.process_command(command)

    def update_game_output(self, text):
        """Update the game output with new descriptions or outcomes."""
        self.game_text_output.append(text)

    def update_inventory(self, items):
        """Update the inventory list."""
        self.inventory_list.clear()
        self.inventory_list.addItems(items)

    def update_status(self, location, health):
        """Update the player's status information."""
        self.location_label.setText(f"Location: {location}")
        self.health_label.setText(f"Health: {health}")
