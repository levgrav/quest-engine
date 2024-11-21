# main.py

from PyQt6.QtWidgets import QApplication
from model import ProjectModel
from view.view_model import ProjectViewModel
from view.view import MainWindow
import sys
from game.world.world import World  



class Game:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.world = World()
        self.model = ProjectModel(self)
        self.view_model = ProjectViewModel(self.model)
        self.window = MainWindow(self.view_model)
    
    def run(self):
        with open("files/stylesheets/style.qss", "r") as file:
            self.app.setStyleSheet(file.read())

        self.window.show()
        sys.exit(self.app.exec())

    def quit(self):
        sys.exit()

if __name__ == "__main__":
    Game().run()