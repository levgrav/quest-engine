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

    def create_button(self, text, width=None, height=None, size=None, callback=None, object_name=None, icon=None):
        """Helper function to create buttons with common styles."""
        button = QPushButton(text)
        if width:
            button.setFixedWidth(width)
        if height:
            button.setFixedHeight(height)
        if size:
            button.setFixedSize(size)
        if callback:
            button.clicked.connect(callback)
        if object_name:
            button.setObjectName(object_name)
        if icon:
            button.setIcon(QIcon(icon))
        return button

    def connect_signals(self): ...
