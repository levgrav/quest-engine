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
    QListWidgetItem,
)
from PyQt6.QtGui import QIcon, QKeySequence, QAction
from PyQt6.QtCore import Qt
import os


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
                widget = QJsonUI(self, value, index.copy())
                layout.addWidget(widget)
            # elif isinstance(value, list):
            #     widget = QListWidget(self)
            #     for item in value:
            #         widget.addItem(QListWidgetItem(widget, self, index, item))
            #     layout.addWidget(widget)
            else:
                widget = QWidget(self)
                widget.setLayout(QHBoxLayout(widget))

                widget.layout().addWidget(QLabel(f"{key}:"))
                j = QJsonValue(widget, self, index.copy(), value)
                self.stuff.append(j)
                widget.layout().addWidget(j)
                layout.addWidget(widget)
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
