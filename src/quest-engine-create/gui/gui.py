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
)
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from PyQt6.QtCore import Qt
import os


class MainWindow(QMainWindow):
    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self.project_name = "cyberpunk_adventure"
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
        self.toggle_json_action = QAction(
            "Toggle &JSON", self, shortcut="Ctrl+J", triggered=self.toggle_json_view
        )
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

        # Left Side Panel - Project Structure Tree
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.project_tree_view = QTreeWidget()
        self.project_tree_view.setHeaderLabels(
            ["Project Structure"]
        )  # Correctly set header labels
        self.populate_project_tree()  # You would define this method to populate the tree
        left_layout.addWidget(self.project_tree_view)
        main_splitter.addWidget(left_panel)

        # Central Tab Widget
        self.create_central_tab_widget()  # Ensure this method sets up self.tab_widget
        main_splitter.addWidget(self.tab_widget)

        # Right Side Panel - AI Interface
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.ai_text_output = QTextEdit()
        self.ai_text_output.setReadOnly(True)
        self.ai_text_input = QLineEdit()
        self.ai_text_input.setPlaceholderText("Enter AI command...")
        self.ai_text_input.returnPressed.connect(self.process_ai_command)
        right_layout.addWidget(self.ai_text_output)
        right_layout.addWidget(self.ai_text_input)
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
        self.setup_npc_editor()
        self.setup_item_editor()
        self.setup_quest_editor()
        self.populate_settings_tab()

    def setup_npc_editor(self):
        layout = QVBoxLayout(
            self.npc_editor
        )  # Assuming `self.npc_editor` is already defined as a QWidget

        # Create the toolbox and sections
        npc_toolbox = QToolBox()
        layout.addWidget(npc_toolbox)
        layout.addWidget(npc_toolbox, alignment=Qt.AlignmentFlag.AlignTop)

        filepath = "files/game_data/game_templates/cyberpunk_adventure/npcs/"

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

        filepath = "files/game_data/game_templates/cyberpunk_adventure/items/"

        # item Templates Section
        item_template_widget = QWidget()
        item_template_layout = QVBoxLayout(item_template_widget)

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

        filepath = "files/game_data/game_templates/cyberpunk_adventure/quests/"

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

    def populate_tab(self, tab_widget, content):
        layout = QVBoxLayout(tab_widget)
        layout.addWidget(QLabel(content))

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
        root_directory = "files/game_data/game_templates/" + self.project_name
        self.project_tree_view.clear()  # Clear existing items if any
        root_item = QTreeWidgetItem(
            self.project_tree_view, [os.path.basename(root_directory)]
        )
        self.add_directory_contents(root_item, root_directory)
        self.project_tree_view.expandAll()  # Optionally expand all nodes

    def add_directory_contents(self, parent_item, directory):
        for entry in os.scandir(directory):
            if entry.is_dir():
                dir_item = QTreeWidgetItem(parent_item, [entry.name])
                self.add_directory_contents(
                    dir_item, entry.path
                )  # Recursive call to add subdirectory contents
            else:
                QTreeWidgetItem(parent_item, [entry.name])  # Add file as child item

    def process_ai_command(self):
        command = self.ai_text_input.text()
        self.ai_text_output.append(f">>> {command}")
        response = f"{self.gui.parent.gpt.process_user_input(command)}"
        self.ai_text_output.append(response)
        temp = self.ai_text_output.toPlainText()
        self.ai_text_input.clear()
        self.init_ui()
        self.ai_text_output.setPlainText(temp)

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


class QJsonWidget(QWidget):
    def __init__(self, display="ui", content=None, filename=None):
        assert display in ["ui", "json"]
        self.display = display
        super().__init__()

        self.content = content

        if filename:
            with open(filename, "r") as file:
                self.content = json.load(file)

        self.init_ui()

    def init_ui(self, layout=None):

        if layout is None:
            self.setLayout(QVBoxLayout(self))
            layout = self.layout()

        self.title = QLabel(self.content.get("name", "Untitled"))

        layout.addWidget(self.title)

        if self.display == "ui":
            self.display_widget = QJsonUI(self, self.content)

        elif self.display == "json":
            self.display_widget = QJsonText(self, self.content)

        layout.addWidget(self.display_widget)

    def set_content(self, content):
        self.content = content
        self.update_ui(),

    def set_content_from_file(self, filename):
        with open(filename, "r") as file:
            self.content = json.load(file)
        self.update_ui(),

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def update_ui(self):
        self.title.setText(self.content.get("name", "Untitled"))
        self.display_widget.set_content(self.content)

    def setWarning(self, warning: bool):
        if warning:
            self.setStyleSheet("border: 1px solid red")
        else:
            self.setStyleSheet("")


class QJsonText(QTextEdit):
    def __init__(self, parent, content=None):
        super().__init__(parent)

        self.content = content
        self.setText(json.dumps(self.content, indent=4))

    def set_content(self, content):
        self.content = content
        self.setText(json.dumps(self.content, indent=4))

    def focusInEvent(self, event):
        self.parent().setMinimumHeight(200)
        self.parent().setCursor(Qt.CursorShape.IBeamCursor)
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        self.parent().setMinimumHeight(100)
        self.parent().setCursor(Qt.CursorShape.ArrowCursor)

        try:
            self.parent().set_content(json.loads(self.toPlainText()))
            self.parent().setWarning(False)
        except json.JSONDecodeError:
            self.parent().setWarning(True)
        super().focusOutEvent(event)


class QJsonUI(QWidget):
    def __init__(self, parent, content=None, index=[]):
        super().__init__(parent)

        self.index = index
        self.content = content

        self.init_ui()

    def init_ui(self, layout=None):
        if layout is None:
            self.setLayout(QVBoxLayout(self))
            layout = self.layout()
        self.stuff = []

        index = self.index.copy()
        for key, value in self.content.items():
            index.append(key)
            if isinstance(value, dict):
                w = QJsonUI(self, value, index.copy())
                layout.addWidget(w)
            elif isinstance(value, list):
                w = QListWidget(self)
                for item in value:
                    w.addItem(QJsonValue(w, self, index, item))
                layout.addWidget(w)
            else:
                w = QWidget(self)
                w.setLayout(QHBoxLayout(w))

                w.layout().addWidget(QLabel(f"{key}:"))
                j = QJsonValue(w, self, index.copy(), value)
                self.stuff.append(j)
                w.layout().addWidget(j)
                layout.addWidget(w)
            index.pop()

    def set_content(self, content):
        self.content = content
        self.parent().title.setText(self.content.get("name", "Untitled"))

    def setWarning(self, warning: bool):
        if warning:
            self.setStyleSheet("border: 1px solid red")
        else:
            self.setStyleSheet("")

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())


class QJsonValue(QLineEdit):

    def __init__(self, parent, json_ui, index, content=None):
        super().__init__(parent)

        self.json_ui = json_ui
        self.index = index
        self.content = content
        self.setText(str(self.content))

    @property
    def value(self):
        val = self.text()
        if val.isdigit():
            val = int(val)
        elif val.replace(".", "", 1).isdigit():
            val = float(val)
        elif val.lower() == "true":
            val = True
        elif val.lower() == "false":
            val = False
        elif val.lower() == "null":
            val = None
        elif val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        elif val.startswith("[") and val.endswith("]"):
            val = val[1:-1].split(", ")
        elif val.startswith("{") and val.endswith("}"):
            val = json.loads(val)

        return val

    def set_content(self, content):
        self.content = content
        self.setText(str(self.content))

    def focusInEvent(self, event):
        super().focusInEvent(event)

    def focusOutEvent(self, event):
        try:
            new_content = self.json_ui.content.copy()
            item = new_content
            for i in range(len(self.index) - 1):
                item = item[self.index[i]]
            item[self.index[-1]] = self.value

            self.json_ui.set_content(new_content)
            self.json_ui.setWarning(False)
        except json.JSONDecodeError:
            self.json_ui.setWarning(True)
        super().focusOutEvent(event)


class Gui:
    def __init__(self, parent):
        self.parent = parent
        self.app = QApplication([])
        self.window = MainWindow(self)

    def run(self):
        self.window.show()
        self.app.exec()
