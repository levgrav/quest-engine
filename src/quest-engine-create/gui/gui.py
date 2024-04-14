from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QToolBar,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTreeWidget,
    QTreeWidgetItem,
    QTextEdit,
    QSplitter,
    QHBoxLayout,
)
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quest Engine Create")
        self.setWindowIcon(QIcon("icon_path.png"))  # Path to your application's icon
        self.setGeometry(100, 100, 1200, 800)  # Adjust size as needed

        self.init_ui()

    def init_ui(self):
        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.setup_main_layout()

    def create_actions(self):
        # File menu actions
        self.new_action = QAction("&New Project", self, shortcut="Ctrl+N")
        self.open_action = QAction("&Open Project...", self, shortcut="Ctrl+O")
        self.save_action = QAction("&Save", self, shortcut="Ctrl+S")
        self.save_as_action = QAction("Save &As...", self, shortcut="Ctrl+Shift+S")
        self.exit_action = QAction(
            "E&xit", self, shortcut="Ctrl+Q", triggered=self.close
        )

        # Edit menu actions
        self.undo_action = QAction("&Undo", self, shortcut="Ctrl+Z")
        self.redo_action = QAction("&Redo", self, shortcut="Ctrl+Y")
        self.cut_action = QAction("Cu&t", self, shortcut="Ctrl+X")
        self.copy_action = QAction("&Copy", self, shortcut="Ctrl+C")
        self.paste_action = QAction("&Paste", self, shortcut="Ctrl+V")

        # Tools menu actions
        self.options_action = QAction("&Options...", self)

        # View menu actions
        self.toggle_sidebar_action = QAction("Toggle &Sidebar", self, shortcut="Ctrl+T")
        self.zoom_in_action = QAction("Zoom &In", self, shortcut="Ctrl++")
        self.zoom_out_action = QAction("Zoom &Out", self, shortcut="Ctrl+-")
        self.reset_zoom_action = QAction("&Reset Zoom", self, shortcut="Ctrl+0")

        # Help menu actions
        self.help_contents_action = QAction("&Contents", self)
        self.about_action = QAction("&About", self)

    def create_menus(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Edit Menu
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction(self.undo_action)
        edit_menu.addAction(self.redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)

        # View Menu
        view_menu = menu_bar.addMenu("&View")
        view_menu.addAction(self.toggle_sidebar_action)
        view_menu.addSeparator()
        view_menu.addAction(self.zoom_in_action)
        view_menu.addAction(self.zoom_out_action)
        view_menu.addAction(self.reset_zoom_action)

        # Tools Menu
        tools_menu = menu_bar.addMenu("&Tools")
        tools_menu.addAction(self.options_action)

        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.help_contents_action)
        help_menu.addSeparator()
        help_menu.addAction(self.about_action)

    def create_toolbar(self):
        toolbar = QToolBar("Toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def setup_main_layout(self):
        main_splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.setCentralWidget(main_splitter)

        # Left Side Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_panel_info = QLabel("Additional Tools")
        left_layout.addWidget(left_panel_info)
        main_splitter.addWidget(left_panel)

        # Central Tab Widget
        self.create_central_tab_widget()
        main_splitter.addWidget(self.tab_widget)

        # Right Side Panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_panel_info = QTextEdit()  # Placeholder for any content
        right_panel_info.setPlainText("Details/Properties Panel")
        right_layout.addWidget(right_panel_info)
        main_splitter.addWidget(right_panel)

        # Setting initial sizes for splitters
        main_splitter.setSizes([200, 800, 200])

    def create_central_tab_widget(self):
        self.tab_widget = QTabWidget()

        self.map_editor = QWidget()
        self.npc_editor = QWidget()
        self.item_editor = QWidget()
        self.quest_editor = QWidget()
        self.settings_editor = QWidget()

        self.tab_widget.addTab(self.map_editor, "Map Editor")
        self.tab_widget.addTab(self.npc_editor, "NPC Editor")
        self.tab_widget.addTab(self.item_editor, "Item Editor")
        self.tab_widget.addTab(self.quest_editor, "Quest Editor")
        self.tab_widget.addTab(self.settings_editor, "Settings")

        # Populate each tab with placeholder content
        self.populate_tab(self.map_editor, "Map Editing Tools Here")
        self.populate_tab(self.npc_editor, "NPC Editing Tools Here")
        self.populate_tab(self.item_editor, "Item Editing Tools Here")
        self.populate_tab(self.quest_editor, "Quest Editing Tools Here")
        self.populate_settings_tab()

    def populate_tab(self, tab_widget, content):
        layout = QVBoxLayout(tab_widget)
        layout.addWidget(QLabel(content))

    def populate_settings_tab(self):
        settings_tree = QTreeWidget(self.settings_editor)
        settings_tree.setHeaderLabel("Settings Categories")
        game_settings = QTreeWidgetItem(settings_tree, ["Game Settings"])
        ui_settings = QTreeWidgetItem(settings_tree, ["UI Settings"])
        ai_settings = QTreeWidgetItem(settings_tree, ["AI Settings"])
        advanced_settings = QTreeWidgetItem(settings_tree, ["Advanced Settings"])
        settings_layout = QVBoxLayout(self.settings_editor)
        settings_layout.addWidget(settings_tree)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
