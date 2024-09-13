# model.py
import json
import ai.gpt as gpt


class ProjectModel:
    def __init__(self, project_name=None, path=""):

        self.parent_dir = r"files\game_data\game_templates"
        self._project_name = project_name
        self.gpt = gpt.Gpt(self)

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, name):
        self._project_name = name

    @property
    def is_project_open(self):
        return self._project_name is not None

    @property
    def path(self):
        if not isinstance(self._project_name, str):
            return self.parent_dir
        return self.parent_dir + "/" + self._project_name

    def process_ai_command(self, command):
        return self.gpt.process_user_input(command)
