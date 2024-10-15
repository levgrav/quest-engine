import os


class Gpt_Functions:

    def __init__(self, project_model) -> None:
        self.project_model = project_model

    def quit_program(
        self,
    ):
        global done
        done = True
        return "Goodbye!"
