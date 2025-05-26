# viewmodel.py

from PyQt6.QtCore import QObject, pyqtSignal
from model import ProjectModel
import os
from view.user_functions import User_Functions


class ProjectViewModel(QObject):
    project_opened = pyqtSignal()  # Signal to notify when a project is opened
    project_closed = pyqtSignal()  # Signal to notify when a project is closed
    ai_response_ready = pyqtSignal(str)

    def __init__(self, model: ProjectModel):
        super().__init__()
        self._model = model
        self.functions = User_Functions(model)

    def open_project(self, project_name: str):
        # Logic to open a project
        if project_name not in os.listdir(self._model.parent_dir):
            return "Project does not exist"
        self._model.project_name = project_name
        self.project_opened.emit()  # Emit signal that a project was opened

    def close_project(self):
        # Logic to close the project
        self._model.project_name = None
        self.project_closed.emit()  # Emit signal that the project was closed

    def create_project(self, project_name: str):
        # Logic to create a new project
        if not project_name:
            return "Please enter a project name"
        self._model.gpt.functions.create_project(project_name)
        self._model.project_name = project_name
        self.project_opened.emit()

    def is_project_open(self):
        return self._model.is_project_open

    def process_ai_command(self, command: str):
        # Process the AI command
        response = self._model.process_ai_command(command)
        self.ai_response_ready.emit(response)

    @property
    def project_name(self):
        return self._model.project_name

    @property
    def path(self):
        return self._model.path
