import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QSplitter, QStackedWidget, QPushButton
)
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

        # Horizontal splitter to separate the left and center panels
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel (Load Game and New Game sections)
        left_panel = QWidget()
        left_panel_layout = QVBoxLayout(left_panel)

        # Load Game section
        load_label = QLabel("Load Game")
        self.saved_games_list = QListWidget()
        self.populate_saved_games()
        left_panel_layout.addWidget(load_label)
        left_panel_layout.addWidget(self.saved_games_list)

        # New Game section
        new_game_label = QLabel("New Game")
        self.game_templates_list = QListWidget()
        self.populate_game_templates()
        left_panel_layout.addWidget(new_game_label)
        left_panel_layout.addWidget(self.game_templates_list)

        # Add left panel to the splitter
        splitter.addWidget(left_panel)

        # Center panel with QStackedWidget for different views
        self.center_panel = QStackedWidget()

        # Default view when nothing is selected
        self.default_view = QWidget()
        default_layout = QVBoxLayout(self.default_view)
        self.default_message_label = QLabel("Select a save or create a new game to play")
        self.default_message_label.setWordWrap(True)
        default_layout.addWidget(self.default_message_label)
        self.center_panel.addWidget(self.default_view)

        # View when a saved game is selected
        self.saved_game_view = QWidget()
        saved_game_layout = QVBoxLayout(self.saved_game_view)
        self.saved_game_info_label = QLabel("Saved game details here")
        self.saved_game_info_label.setWordWrap(True)
        self.saved_game_play_button = self.create_button(
            "Play Game", 545, lambda: self.view_model.show_page("game")
        )
        saved_game_layout.addWidget(self.saved_game_info_label)
        saved_game_layout.addWidget(self.saved_game_play_button)
        self.center_panel.addWidget(self.saved_game_view)

        # View when a game template is selected
        self.template_view = QWidget()
        template_layout = QVBoxLayout(self.template_view)
        self.template_info_label = QLabel("Game template details here")
        self.template_info_label.setWordWrap(True)
        self.template_create_button = self.create_button(
            "Create Game", 545, lambda: self.view_model.show_page("game")
        )
        template_layout.addWidget(self.template_info_label)
        template_layout.addWidget(self.template_create_button)
        self.center_panel.addWidget(self.template_view)

        # Set the default view as the current view
        self.center_panel.setCurrentWidget(self.default_view)

        # Add center panel (QStackedWidget) to the splitter
        splitter.addWidget(self.center_panel)

        # Add the splitter to the main layout
        layout.addWidget(splitter)

        # Back button
        self.back_button = self.create_button(
            "Back", 545, lambda: self.view_model.show_page("main_menu")
        )
        layout.addWidget(self.back_button, alignment=Qt.AlignmentFlag.AlignCenter)

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

    def on_selection_changed(self):
        """Handle when a saved game or template is selected."""
        selected_saved_game = self.saved_games_list.selectedItems()
        selected_template = self.game_templates_list.selectedItems()

        # Prioritize handling new selections
        if self.saved_games_list.hasFocus() and selected_saved_game:
            # Clear the template selection if a saved game was selected
            self.game_templates_list.clearSelection()

            # Display details about the selected saved game
            file_name = selected_saved_game[0].text()
            self.show_file_details(
                f"files/game_data/saves/games/{file_name}", is_template=False
            )
        elif self.game_templates_list.hasFocus() and selected_template:
            # Clear the saved game selection if a game template was selected
            self.saved_games_list.clearSelection()

            # Display details about the selected template
            file_name = selected_template[0].text()
            self.show_file_details(
                f"files/game_data/game_templates/{file_name}", is_template=True
            )
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
