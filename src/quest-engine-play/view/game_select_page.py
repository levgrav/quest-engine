import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QSplitter, QStackedWidget, QPushButton, QHBoxLayout, QFrame
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from view.page import Page


class GameSelectPage(Page):
    def __init__(self, view_model, parent, stacked_widget):
        super().__init__(
            view_model=view_model,
            parent=parent,
            stacked_widget=stacked_widget,
            page_name="game_select",
        )

    def init_ui(self):
        """Initialize the UI layout for the Game Select page."""
        layout = QVBoxLayout(self)

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
        
        # Add the top bar to the main layout
        layout.addWidget(top_bar)

        # --- Horizontal Splitter: Left Panel and Center Panel ---
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel (Load Game and New Game sections)
        left_panel = QWidget()
        left_panel_layout = QVBoxLayout(left_panel)

        # Load Game section
        load_label = QLabel("Load Game")
        load_label.setObjectName("section_label")
        self.saved_games_list = QListWidget()
        self.populate_saved_games()
        left_panel_layout.addWidget(load_label)
        left_panel_layout.addWidget(self.saved_games_list)

        # New Game section
        new_game_label = QLabel("New Game")
        new_game_label.setObjectName("section_label")
        self.game_templates_list = QListWidget()
        self.populate_game_templates()
        left_panel_layout.addWidget(new_game_label)
        left_panel_layout.addWidget(self.game_templates_list)

        # --- Download More Content Button ---
        download_button = QPushButton("Download More Content")
        download_button.setObjectName("download_button")
        download_button.clicked.connect(self.download_more_content)  # Dummy function
        left_panel_layout.addWidget(download_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add left panel to the splitter
        splitter.addWidget(left_panel)

        # --- Framed Center Panel with Shades ---
        center_panel_frame = QFrame()
        center_panel_frame.setObjectName("center_panel_frame")
        center_panel_layout = QVBoxLayout(center_panel_frame)

        # Center panel title with a slightly lighter background
        center_panel_title_frame = QWidget()
        center_panel_title_frame.setObjectName("center_panel_title_frame")
        center_panel_title_layout = QVBoxLayout(center_panel_title_frame)
        center_panel_title = QLabel("Game Details")
        center_panel_title.setObjectName("center_panel_title")
        center_panel_title_layout.addWidget(center_panel_title, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the title frame to the center panel layout
        center_panel_layout.addWidget(center_panel_title_frame)

        # Center panel with QStackedWidget for dynamic content
        self.center_panel = QStackedWidget()

        # Default view when nothing is selected
        self.default_view = QWidget()
        default_layout = QVBoxLayout(self.default_view)
        self.default_message_label = QLabel("Select a save or create a new game to play")
        self.default_message_label.setObjectName("default_message")
        default_layout.addWidget(self.default_message_label)
        self.center_panel.addWidget(self.default_view)

        # View when a saved game is selected
        self.saved_game_view = QWidget()
        saved_game_layout = QVBoxLayout(self.saved_game_view)
        self.saved_game_info_label = QLabel("Saved game details here")
        self.saved_game_info_label.setObjectName("saved_game_info")
        self.saved_game_play_button = self.create_button(
            "Play Game", 545, callback=lambda: self.view_model.show_page("game"), object_name="play_button"
        )
        saved_game_layout.addWidget(self.saved_game_info_label)
        saved_game_layout.addWidget(self.saved_game_play_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.center_panel.addWidget(self.saved_game_view)

        # View when a game template is selected
        self.template_view = QWidget()
        template_layout = QVBoxLayout(self.template_view)
        self.template_info_label = QLabel("Game template details here")
        self.template_create_button = self.create_button(
            "Create Game", 545, callback=lambda: self.view_model.show_page("game"), object_name="create_game_button"
        )
        template_layout.addWidget(self.template_info_label)
        template_layout.addWidget(self.template_create_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.center_panel.addWidget(self.template_view)

        # Set the default view as the current view
        self.center_panel.setCurrentWidget(self.default_view)

        # Add center panel (QStackedWidget) to the framed layout
        center_panel_layout.addWidget(self.center_panel)

        # Add the framed center panel to the splitter
        splitter.addWidget(center_panel_frame)

        # Add the splitter to the main layout
        layout.addWidget(splitter)

        self.setLayout(layout)

        # Connect list item selections to the handler
        self.saved_games_list.itemSelectionChanged.connect(self.on_selection_changed)
        self.game_templates_list.itemSelectionChanged.connect(self.on_selection_changed)

    def populate_saved_games(self):
        """Populate the saved games list from the directory."""
        saves_path = "files/game_data/saves/games"
        if os.path.exists(saves_path):
            for file_name in os.listdir(saves_path):
                if file_name.endswith(".save"):  # Assuming saved games have a .save extension
                    self.saved_games_list.addItem(file_name)

    def populate_game_templates(self):
        """Populate the game templates list from the directory."""
        templates_path = "files/game_data/game_templates"
        if os.path.exists(templates_path):
            for file_name in os.listdir(templates_path):
                if file_name.endswith(".template"):  # Assuming templates have a .template extension
                    self.game_templates_list.addItem(file_name)

    def download_more_content(self):
        """Handle the download content button click."""
        print("Download More Content button clicked!")

    def on_selection_changed(self):
        """Handle when a saved game or template is selected."""
        selected_saved_game = self.saved_games_list.selectedItems()
        selected_template = self.game_templates_list.selectedItems()

        if self.saved_games_list.hasFocus() and selected_saved_game:
            # Clear the template selection
            self.game_templates_list.clearSelection()

            # Display details about the selected saved game
            file_name = selected_saved_game[0].text()
            self.show_file_details(f"files/game_data/saves/games/{file_name}", is_template=False)
        elif self.game_templates_list.hasFocus() and selected_template:
                        # Clear the saved game selection
            self.saved_games_list.clearSelection()

            # Display details about the selected template
            file_name = selected_template[0].text()
            self.show_file_details(f"files/game_data/game_templates/{file_name}", is_template=True)
        else:
            # Nothing selected, show default message
            self.center_panel.setCurrentWidget(self.default_view)

    def show_file_details(self, file_path, is_template):
        """Show details about the selected file."""
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                details = file.read()  # Example of reading file contents

            # Switch to the appropriate view and display details
            if is_template:
                self.template_info_label.setText(details)
                self.center_panel.setCurrentWidget(self.template_view)
            else:
                self.saved_game_info_label.setText(details)
                self.center_panel.setCurrentWidget(self.saved_game_view)

