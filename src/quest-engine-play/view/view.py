from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QComboBox,
)
from PyQt6.QtGui import QIcon, QPixmap, QPainter
import ctypes
import sys
from view.page import Page
from view.game_page import GamePage
from view.main_menu_page import MainMenuPage
from view.game_select_page import GameSelectPage
from PyQt6.QtCore import Qt, qInstallMessageHandler, QtMsgType


# Custom message handler to suppress warnings
def suppress_qt_warnings(msg_type, context, message):
    if msg_type == QtMsgType.QtWarningMsg:
        # Suppress all warnings
        pass
    else:
        # Pass other types of messages through
        print(message)


# Install the message handler
qInstallMessageHandler(suppress_qt_warnings)


class MainWindow(QMainWindow):
    def __init__(self, view_model, **kwargs):
        super().__init__()

        self.view_model = view_model
        self.setWindowTitle("Quest Engine Play")

        self.setWindowIcon(QIcon(r"files/icon/icon.svg"))
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

        # Fullscreen and window geometry
        self.setGeometry(100, 100, 1200, 800)
        self.showFullScreen()

        # Load the background image once
        self.background_image = QPixmap()

        # Initialize the UI
        self.init_pages()
        self.connect_signals()
        self.view_model.show_page("main_menu")

    def init_pages(self):
        """Initialize the UI components, including the main menu and game page."""
        # Stacked widget to switch between main menu and game page
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.game_page = GamePage(
            self.view_model, parent=self, stacked_widget=self.stacked_widget
        )
        self.main_menu_page = MainMenuPage(
            self.view_model, parent=self, stacked_widget=self.stacked_widget
        )
        self.game_select_page = GameSelectPage(
            self.view_model, parent=self, stacked_widget=self.stacked_widget
        )

    def keyPressEvent(self, event):
        """Override keyPressEvent to toggle fullscreen with F11."""
        if event.key() == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()  # Exit fullscreen
            else:
                self.showFullScreen()  # Enter fullscreen
        else:
            super().keyPressEvent(event)  # Pass other key presses to the base class

    def show_page(self, page: Page):
        """Show the selected page."""
        self.stacked_widget.setCurrentWidget(page)
        self.background_image = QPixmap(page.background_image_path)

    def connect_signals(self):
        """Connect signals here if needed."""
        self.view_model.page_shown.connect(self.show_page)

    def resizeEvent(self, event):
        """Ensure the background image is resized when the page is resized."""
        self.update()  # Trigger repaint
        super().resizeEvent(event)

    def paintEvent(self, event):
        """Override paintEvent to paint the background image."""
        painter = QPainter(self)
        scaled_image = self.background_image.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        x = (self.size().width() - scaled_image.width()) // 2
        y = (self.size().height() - scaled_image.height()) // 2
        painter.drawPixmap(x, y, scaled_image)
