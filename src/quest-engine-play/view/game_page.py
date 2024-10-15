from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget, 
    QSplitter, QListWidget, QLabel, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon
from view.page import Page

class GamePage(Page):
    def __init__(self, view_model, parent, stacked_widget):
        super().__init__(view_model, parent, stacked_widget, "game")

    def init_ui(self):
        """Initialize the game window layout."""
        # Top Bar with Back Button, Logo, and Settings Button
        top_bar = self.init_top_bar()

        # Main horizontal splitter for panels
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Initialize the panels
        self.init_left_panel(main_splitter)    # Left: Inventory
        self.init_center_panel(main_splitter)  # Center: Story Log
        self.init_right_panel(main_splitter)   # Right: Player Status

        # Main layout with top bar, panels, and bottom actions
        layout = QVBoxLayout()
        layout.addWidget(top_bar)
        layout.addWidget(main_splitter)
        
        # Set the layout to the widget
        self.setLayout(layout)

    def init_top_bar(self):
        """Create a top bar with a Back button, Logo, and Settings button."""
        # --- Top Bar: Logo (Left) and Back Button (Right) ---
        top_bar = QWidget()
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(20, 15, 20, 15)  # Increased margins
        top_bar_layout.setSpacing(10)

        # Limit the height of the top bar
        top_bar.setFixedHeight(120)

        # --- Logo Overlay on the Left ---
        overlay = QWidget(top_bar)
        overlay.setObjectName("overlay")
        overlay_layout = QHBoxLayout(overlay)
        overlay_layout.setContentsMargins(20, 10, 20, 10)  # Adjusted inner padding

        # Icon (Q)
        icon_label = QLabel(self)
        pixmap = QPixmap("files/icon/icon_transparent.svg").scaled(
            60, 60, Qt.AspectRatioMode.KeepAspectRatio
        )
        icon_label.setPixmap(pixmap)
        overlay_layout.addWidget(icon_label)

        # Title ("uest Engine")
        title_label = QLabel("uest Engine")
        title_label.setObjectName("small_title")
        overlay_layout.addWidget(title_label)

        # Add the logo (overlay) to the top bar on the left
        top_bar_layout.addWidget(overlay)
        top_bar_layout.addStretch()

        # --- Back Button (Right) ---
        self.back_button = self.create_button(
            "Back", width=150, callback=lambda: self.view_model.show_page("main_menu"), object_name="back_button"
        )
        top_bar_layout.addWidget(self.back_button)

        self.settings_button = self.create_button(
            "", width=55, height=55, object_name="settings_button", icon="files/icon/settings.svg"
        )
        self.settings_button.setIconSize(self.settings_button.size() * 0.5)
        top_bar_layout.addWidget(self.settings_button)
        
        return top_bar

    def init_left_panel(self, main_splitter):
        """Setup the left panel (Inventory)."""
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)

        # Inventory Label and List
        inventory_label = QLabel("Inventory")
        self.inventory_list = QListWidget()

        left_layout.addWidget(inventory_label)
        left_layout.addWidget(self.inventory_list)

        # Add the panel to the splitter
        main_splitter.addWidget(left_panel)

    def init_center_panel(self, main_splitter):
        """Setup the center panel (Game Output and Command Input)."""
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)

        # Story Log (Game Output)
        self.game_text_output = QTextEdit()
        self.game_text_output.setReadOnly(True)

        # Command Input
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Enter your command...")

        center_layout.addWidget(self.game_text_output)
        center_layout.addWidget(self.command_input)

        # Add the center panel to the splitter
        main_splitter.addWidget(center_panel)

        # Give the center panel more space than the others
        main_splitter.setStretchFactor(1, 3)

    def init_right_panel(self, main_splitter):
        """Setup the right panel (Player Status and Stats)."""
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # Player Status Labels
        status_label = QLabel("Player Status")
        self.location_label = QLabel("Location: Unknown")
        self.health_label = QLabel("Health: 100")

        # Quest Progress List
        quest_progress_label = QLabel("Quest Progress")
        self.quest_list = QListWidget()
        self.quest_list.addItems(["Find the Amulet", "Defeat the Dragon"])

        right_layout.addWidget(status_label)
        right_layout.addWidget(self.location_label)
        right_layout.addWidget(self.health_label)
        right_layout.addWidget(quest_progress_label)
        right_layout.addWidget(self.quest_list)

        # Add the panel to the splitter
        main_splitter.addWidget(right_panel)

    
    def connect_signals(self):
        """Connect signals for user interaction."""
        # Execute command when 'Enter' is pressed in the input field
        self.command_input.returnPressed.connect(self.process_command)
        self.view_model.ai_response_ready.connect(self.update_game_output)

    def process_command(self):
        """Handle the user’s input command."""
        command = self.command_input.text()
        self.command_input.clear()  # Clear the input field

        # Display the entered command in the story log
        self.game_text_output.append(f">>> {command}")

        # Process the command through the view model
        self.view_model.process_command(command)

    def update_game_output(self, text):
        """Update the story log with new game events."""
        self.game_text_output.append(text)

    def update_inventory(self, items):
        """Update the inventory list with new items."""
        self.inventory_list.clear()
        self.inventory_list.addItems(items)

    def update_status(self, location, health):
        """Update the player's status with new values."""
        self.location_label.setText(f"Location: {location}")
        self.health_label.setText(f"Health: {health}")

    def update_quests(self, quests):
        """Update the quest progress with new quests."""
        self.quest_list.clear()
        self.quest_list.addItems(quests)
