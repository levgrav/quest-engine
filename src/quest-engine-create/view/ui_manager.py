import json
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
    QToolBox,
    QFormLayout,
    QCheckBox,
    QSpinBox,
    QPushButton,
    QColorDialog,
    QLineEdit,
    QListWidget,
    QInputDialog,
)
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from PyQt6.QtCore import Qt
import os
from view.json_components import QJsonWidget


class UIManager:

    def __init__(self, window):
        self.window = window
        self.init_ui()

    def init_ui(self):
        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.setup_main_layout()

    def update_ui(self):
        self.project_tree_view.clear()

        tab_index = self.tab_widget.currentIndex()

        self.tab_widget.clear()

        if self.window.view_model.is_project_open():
            self.populate_project_tree()
            self.create_central_tab_widget_open()
        else:
            self.populate_project_tree_closed()
            self.create_central_tab_widget_closed()

        self.tab_widget.setCurrentIndex(tab_index)

    def create_actions(self):
        # File menu actions
        self.create_action = QAction("&New Project", self.window, shortcut="Ctrl+N")
        self.open_action = QAction("&Open Project...", self.window, shortcut="Ctrl+O")
        self.save_action = QAction("&Save", self.window, shortcut="Ctrl+S")
        self.save_as_action = QAction(
            "Save &As...", self.window, shortcut="Ctrl+Shift+S"
        )
        self.exit_action = QAction(
            "E&xit", self.window, shortcut="Ctrl+Q", triggered=self.window.close
        )
        self.close_action = QAction("&Close Project", self.window)

        # Edit menu actions
        self.undo_action = QAction("&Undo", self.window, shortcut="Ctrl+Z")
        self.redo_action = QAction("&Redo", self.window, shortcut="Ctrl+Y")
        self.cut_action = QAction("Cu&t", self.window, shortcut="Ctrl+X")
        self.copy_action = QAction("&Copy", self.window, shortcut="Ctrl+C")
        self.paste_action = QAction("&Paste", self.window, shortcut="Ctrl+V")

        # Tools menu actions
        self.options_action = QAction("&Options...", self.window)

        # View menu actions
        self.toggle_json_action = QAction(
            "Toggle &JSON",
            self.window,
            shortcut="Ctrl+J",
            triggered=self.toggle_json_view,
        )
        self.toggle_sidebar_action = QAction(
            "Toggle &Sidebar", self.window, shortcut="Ctrl+T"
        )
        self.zoom_in_action = QAction("Zoom &In", self.window, shortcut="Ctrl++")
        self.zoom_out_action = QAction("Zoom &Out", self.window, shortcut="Ctrl+-")
        self.reset_zoom_action = QAction("&Reset Zoom", self.window, shortcut="Ctrl+0")

        # Help menu actions
        self.help_contents_action = QAction("&Contents", self.window)
        self.about_action = QAction("&About", self.window)

    def create_menus(self):
        menu_bar = self.window.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.create_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.close_action)
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
        view_menu.addAction(self.toggle_json_action)
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
        self.window.addToolBar(toolbar)
        toolbar.addAction(self.create_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.close_action)
        toolbar.addAction(self.save_action)
        toolbar.addAction(self.save_as_action)
        toolbar.addSeparator()
        toolbar.addAction(self.undo_action)
        toolbar.addAction(self.redo_action)
        toolbar.addSeparator()
        toolbar.addAction(self.cut_action)
        toolbar.addAction(self.copy_action)
        toolbar.addAction(self.paste_action)
        toolbar.addSeparator()
        toolbar.addAction(self.toggle_json_action)
        toolbar.addAction(self.toggle_sidebar_action)
        toolbar.addSeparator()
        toolbar.addAction(self.zoom_in_action)
        toolbar.addAction(self.zoom_out_action)
        toolbar.addAction(self.reset_zoom_action)

    def create_status_bar(self):
        status_bar = QStatusBar()
        self.window.setStatusBar(status_bar)
        status_bar.showMessage("Ready")

    def setup_main_layout(self):
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal, self.window)
        self.window.setCentralWidget(self.main_splitter)

        # Left Side Panel - Project Structure Tree
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.project_tree_view = QTreeWidget()

        if self.window.view_model.is_project_open():
            self.project_tree_view.setHeaderLabels(
                [f"Project Structure: {self.window.view_model.project_name}"]
            )
            self.populate_project_tree()
        else:
            self.project_tree_view.setHeaderLabels(["Projects"])
            self.populate_project_tree_closed()

        left_layout.addWidget(self.project_tree_view)
        self.main_splitter.addWidget(left_panel)

        # Central Tab Widget
        self.tab_widget = QTabWidget()

        if self.window.view_model.is_project_open():
            self.create_central_tab_widget_open()
        else:
            self.create_central_tab_widget_closed()
        self.main_splitter.addWidget(self.tab_widget)

        """Set up the right side AI interface panel with input/output fields."""
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        # AI Output (QTextEdit) - read-only for displaying AI responses
        self.ai_text_output = QTextEdit()
        self.ai_text_output.setReadOnly(True)

        # AI Input (QLineEdit) - user enters commands here
        self.ai_text_input = QLineEdit()
        self.ai_text_input.setPlaceholderText("Enter AI command...")

        # Add the widgets to the right panel's layout
        right_layout.addWidget(self.ai_text_output)
        right_layout.addWidget(self.ai_text_input)

        # Add the right panel to the main splitter
        self.main_splitter.addWidget(right_panel)

        # Setting initial sizes for splitters
        self.main_splitter.setSizes([200, 800, 200])

    def create_central_tab_widget_open(self):
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

        self.populate_tab_placeholder(self.map_editor, "Map Editing Tools Here")
        self.setup_npc_editor()
        self.setup_item_editor()
        self.setup_quest_editor()
        self.populate_settings_tab()

    def create_central_tab_widget_closed(self):
        self.tab_widget.addTab(QWidget(), "Welcome")
        self.tab_widget.addTab(QWidget(), "Recent Projects")
        self.tab_widget.addTab(QWidget(), "Tutorials")

        self.populate_tab_placeholder(
            self.tab_widget.widget(0), "Welcome to Quest Engine Create!"
        )
        self.populate_tab_placeholder(
            self.tab_widget.widget(1), "No recent projects to display."
        )
        self.populate_tab_placeholder(
            self.tab_widget.widget(2), "Tutorials coming soon!"
        )

    def populate_tab_placeholder(self, tab_widget, message):
        layout = QVBoxLayout(tab_widget)
        layout.addWidget(QLabel(message), alignment=Qt.AlignmentFlag.AlignCenter)

    def populate_settings_tab(self):
        settings_layout = QVBoxLayout(self.settings_editor)
        settings_toolbox = QToolBox()
        settings_layout.addWidget(settings_toolbox, alignment=Qt.AlignmentFlag.AlignTop)

        # General Settings
        general_settings_widget = QWidget()
        general_layout = QFormLayout()
        autosave_checkbox = QCheckBox("Enable Autosave")
        general_layout.addRow("Autosave:", autosave_checkbox)
        autosave_interval_spinbox = QSpinBox()
        autosave_interval_spinbox.setRange(1, 60)  # in minutes
        general_layout.addRow("Autosave Interval (minutes):", autosave_interval_spinbox)
        general_settings_widget.setLayout(general_layout)
        settings_toolbox.addItem(general_settings_widget, "General Settings")

        # UI Customizations
        ui_settings_widget = QWidget()
        ui_layout = QVBoxLayout()
        theme_button = QPushButton("Change Theme Color")
        theme_button.clicked.connect(self.change_theme_color)
        ui_layout.addWidget(theme_button)
        ui_settings_widget.setLayout(ui_layout)
        settings_toolbox.addItem(ui_settings_widget, "UI Customizations")

        # Game Mechanics
        game_mechanics_widget = QWidget()
        mechanics_layout = QVBoxLayout()
        enable_dlc_checkbox = QCheckBox("Enable DLC Content")
        mechanics_layout.addWidget(enable_dlc_checkbox)
        game_mechanics_widget.setLayout(mechanics_layout)
        settings_toolbox.addItem(game_mechanics_widget, "Game Mechanics")

        # Script Settings
        script_settings_widget = QWidget()
        script_layout = QVBoxLayout()
        enable_debug_mode_checkbox = QCheckBox("Enable Script Debug Mode")
        script_layout.addWidget(enable_debug_mode_checkbox)
        script_settings_widget.setLayout(script_layout)
        settings_toolbox.addItem(script_settings_widget, "Script Settings")

    def populate_project_tree(self):

        self.project_tree_view.clear()  # Clear existing items if any
        root_item = QTreeWidgetItem(
            self.project_tree_view, [os.path.basename(self.window.view_model.path)]
        )
        self.add_directory_contents(root_item, self.window.view_model.path)
        self.project_tree_view.expandAll()

    def populate_project_tree_closed(self):  # only displays project folders
        self.project_tree_view.clear()
        for entry in os.scandir(self.window.view_model._model.parent_dir):
            QTreeWidgetItem(self.project_tree_view, [entry.name])

    def add_directory_contents(self, parent_item, directory):
        try:
            for entry in os.scandir(directory):
                if entry.is_dir():
                    dir_item = QTreeWidgetItem(parent_item, [entry.name])
                    self.add_directory_contents(
                        dir_item, entry.path
                    )  # Recursive call to add subdirectory contents
                else:
                    QTreeWidgetItem(parent_item, [entry.name])  # Add file as child item
        except FileNotFoundError:
            print(f"Error: Directory {directory} not found")

    def change_theme_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"Chosen color: {color.name()}")  # Example action

    def toggle_json_view(self):
        current_tab = self.tab_widget.currentWidget()
        if isinstance(current_tab, QWidget):
            json_widgets = current_tab.findChildren(QJsonWidget)
            for widget in json_widgets:
                if widget.display == "json":
                    widget.display = "ui"
                else:
                    widget.display = "json"
                widget.clear_layout(widget.layout())
                widget.init_ui(widget.layout())

    def setup_npc_editor(self):
        layout = QVBoxLayout(self.npc_editor)

        # Create the toolbox and sections
        npc_toolbox = QToolBox()
        layout.addWidget(npc_toolbox)
        layout.addWidget(npc_toolbox, alignment=Qt.AlignmentFlag.AlignTop)

        filepath = self.window.view_model.path + "/npcs/"

        # NPC Templates Section
        npc_template_widget = QWidget()
        npc_template_layout = QVBoxLayout(npc_template_widget)

        for root, dirs, files in os.walk(filepath + "template"):
            for file in files:
                if file.endswith(".json"):

                    npc_template_layout.addWidget(
                        QJsonWidget(display="ui", filename=os.path.join(root, file))
                    )

        # Button for adding new NPC Templates
        new_npc_template_button = QPushButton("+ New")
        new_npc_template_button.clicked.connect(self.add_new_npc_template)
        npc_template_layout.addWidget(new_npc_template_button)

        npc_toolbox.addItem(npc_template_widget, "NPC Templates")

        # Custom NPCs Section
        custom_npc_widget = QWidget()
        custom_npc_layout = QVBoxLayout(custom_npc_widget)

        for root, dirs, files in os.walk(filepath + "custom"):
            for file in files:
                if file.endswith(".json"):
                    custom_npc_layout.addWidget(
                        QJsonWidget(display="ui", filename=os.path.join(root, file))
                    )

        # Button for adding new Custom NPCs
        new_custom_npc_button = QPushButton("+ New")
        new_custom_npc_button.clicked.connect(self.add_new_custom_npc)
        custom_npc_layout.addWidget(new_custom_npc_button)

        npc_toolbox.addItem(custom_npc_widget, "Custom NPCs")

    def add_new_custom_npc(self):
        # Placeholder method for adding a new Custom NPC
        print("Adding new Custom NPC...")

    def add_new_npc_template(self):
        # Placeholder method for adding a new NPC Template
        print("Adding new NPC Template...")

    def setup_item_editor(self):
        layout = QVBoxLayout(self.item_editor)

        # Create the toolbox and sections
        item_toolbox = QToolBox()
        layout.addWidget(item_toolbox)
        layout.addWidget(item_toolbox, alignment=Qt.AlignmentFlag.AlignTop)

        # item Templates Section
        item_template_widget = QWidget()
        item_template_layout = QVBoxLayout(item_template_widget)

        filepath = self.window.view_model.path + "/items/"

        for root, dirs, files in os.walk(filepath + "template"):
            for file in files:
                if file.endswith(".json"):

                    item_template_layout.addWidget(
                        QJsonWidget(display="ui", filename=os.path.join(root, file))
                    )

        # Button for adding new item Templates
        new_item_template_button = QPushButton("+ New")
        new_item_template_button.clicked.connect(self.add_new_item_template)
        item_template_layout.addWidget(new_item_template_button)

        item_toolbox.addItem(item_template_widget, "Item Templates")

        # Custom items Section
        custom_item_widget = QWidget()
        custom_item_layout = QVBoxLayout(custom_item_widget)

        for root, dirs, files in os.walk(filepath + "custom"):
            for file in files:
                if file.endswith(".json"):
                    custom_item_layout.addWidget(
                        QJsonWidget(display="ui", filename=os.path.join(root, file))
                    )

        # Button for adding new Custom items
        new_custom_item_button = QPushButton("+ New")
        new_custom_item_button.clicked.connect(self.add_new_custom_item)
        custom_item_layout.addWidget(new_custom_item_button)

        item_toolbox.addItem(custom_item_widget, "Custom Items")

    def add_new_custom_item(self):
        # Placeholder method for adding a new Custom item
        print("Adding new Custom Item...")

    def add_new_item_template(self):
        # Placeholder method for adding a new Item Template
        print("Adding new Item Template...")

    def setup_quest_editor(self):
        layout = QVBoxLayout(self.quest_editor)

        filepath = self.window.view_model.path + "/quests/"

        for root, dirs, files in os.walk(filepath):
            for file in files:
                if file.endswith(".json"):

                    layout.addWidget(
                        QJsonWidget(display="ui", filename=os.path.join(root, file))
                    )

        # Button for adding new quest Templates
        new_quest_button = QPushButton("+ New")
        new_quest_button.clicked.connect(self.add_new_quest)
        layout.addWidget(new_quest_button)

    def add_new_quest(self):
        # Placeholder method for adding a new Quest
        print("Adding new Quest...")

    def text_prompt(self, title, prompt):
        # creates a dialog box with a text input field
        text, ok = QInputDialog.getText(self.window, title, prompt)
        if ok:
            return text
