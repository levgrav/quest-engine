# main.py

from PyQt6.QtWidgets import QApplication
from model import ProjectModel
from view.viewmodel import ProjectViewModel
from view.view import MainWindow
import sys


def main():
    app = QApplication(sys.argv)

    # Initialize the model
    model = ProjectModel()

    # Initialize the View-Model and pass the model
    view_model = ProjectViewModel(model)

    # Initialize the MainWindow (View) and pass the View-Model
    window = MainWindow(view_model)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
