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
    QStackedWidget,
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtCore import Qt


class Page(QWidget):

    background_image_path = None

    def __init__(self, view_model, parent, stacked_widget: QStackedWidget, page_name):
        super().__init__()
        self.view_model = view_model
        self.parent = parent

        stacked_widget.addWidget(self)
        self.view_model.register_page(page_name, self)

        self.init_ui()
        self.connect_signals()

    def init_ui(self): ...

    def create_button(self, text, width, callback=None):
        """Helper function to create buttons with common styles."""
        button = QPushButton(text)
        button.setFixedWidth(width)
        button.setStyleSheet(
            """
            font-size: 27px;
            font-weight: bold;
            font-family: 'Open Sans';
            padding: 20px 10px;
            color: white;
            background-color: rgba(0, 0, 0, 0.6);
            border: 2px solid white;
            border-radius: 10px;
        """
        )
        if callback:
            button.clicked.connect(callback)
        return button

    def connect_signals(self): ...
