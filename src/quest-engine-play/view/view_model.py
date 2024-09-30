# viewmodel.py
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget


class ProjectViewModel(QObject):
    debug_info = pyqtSignal(str)
    ai_response_ready = pyqtSignal(str)  # Signal to notify new game text
    page_shown = pyqtSignal(QWidget)

    def __init__(self, model):
        super().__init__()
        self._model = model
        self.pages = {}
        self.debug_info.connect(print)
        self.debug_info.emit("View Model Initialized...")

    def register_page(self, page_name, page):
        """Register the page with the view model."""
        self.pages[page_name] = page

    def show_page(self, page_name):
        """Show the selected page."""
        # Logic to show the page
        if page_name in self.pages:
            page = self.pages[page_name]
            self.debug_info.emit(f"Showing {page_name}...")
            self.page_shown.emit(page)
        else:
            self.debug_info.emit(f"Page {page_name} not found!")

    def start_game(self, game_name):
        """Start the selected game."""
        # Logic to start the game
        self.debug_info.emit(f"Starting {game_name}...")

    def process_command(self, command):
        """Process the command entered by the player."""
        # Interact with the model for game logic
        response = self._model.process_command(command)
        self.ai_response_ready.emit(response)
