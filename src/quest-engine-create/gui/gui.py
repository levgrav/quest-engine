from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QLineEdit,
    QLabel,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QHBoxLayout,
    QSplitter,
    QMessageBox,
    QScrollArea,
)
from PyQt6.QtGui import QIcon, QKeySequence, QAction, QPixmap
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Quest Engine Play")
        self.setWindowIcon(
            QIcon("path/to/your/icon.png")
        )  # Set the path to your application icon
        self.setGeometry(
            100, 100, 1200, 800
        )  # Adjust initial size to provide more room

        self.setup_ui()
        self.showMaximized()  # Make the main window open in maximized state

    def setup_ui(self):
        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.create_main_layout()

    def create_actions(self):
        self.exit_action = QAction("&Exit", self)
        self.exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        self.exit_action.triggered.connect(self.close)

        self.about_action = QAction("&About", self)
        self.about_action.triggered.connect(self.about)

    def create_menus(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.exit_action)

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.about_action)

    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(self.exit_action)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def create_main_layout(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left Panel: Map and Encyclopedia/World Data
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.map_label = QLabel()
        map_pixmap = QPixmap("files/icon/icon0.625.png")
        self.map_label.setPixmap(map_pixmap)
        left_layout.addWidget(self.map_label)

        # Tabs for Encyclopedia and World Data
        info_tabs = QTabWidget()
        encyclopedia_tab = QWidget()  # Placeholder for actual content
        world_data_tab = QWidget()  # Placeholder for actual content
        info_tabs.addTab(encyclopedia_tab, "Encyclopedia")
        info_tabs.addTab(world_data_tab, "World Data")
        left_layout.addWidget(info_tabs)

        # Center Panel: Game Text and Command Line
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        self.game_text_edit = QTextEdit()
        self.game_text_edit.setReadOnly(True)
        center_layout.addWidget(self.game_text_edit)
        self.command_line_edit = QLineEdit()
        self.command_line_edit.setPlaceholderText("Enter command...")
        center_layout.addWidget(self.command_line_edit)

        # Right Panel: Character Stats and Inventory
        char_widget = QWidget()
        char_layout = QVBoxLayout(char_widget)

        # Character Image above Tabs
        char_image_label = QLabel()
        char_pixmap = QPixmap("files/icon/icon0.625.png")
        char_image_label.setPixmap(char_pixmap)
        char_layout.addWidget(char_image_label)

        # Tabs for Stats and Inventory
        tabs = QTabWidget()
        tabs.addTab(QLabel("Character Stats"), "Stats")
        tabs.addTab(QLabel("Inventory"), "Inventory")
        char_layout.addWidget(tabs)

        # Splitter Setup
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(center_widget)
        splitter.addWidget(char_widget)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)
        main_layout.addWidget(splitter)

    def about(self):
        QMessageBox.about(self, "About", "Quest Engine Play\nDeveloped by [Your Name]")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()
