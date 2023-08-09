import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QDockWidget, QTreeView, QTextEdit, QLineEdit, QFileDialog, QMenuBar, QFileSystemModel
from PySide6.QtGui import QAction

from PySide6.QtCore import Qt, QDir

import openai


def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose an appropriate engine
        prompt=prompt,
        max_tokens=4000  # Adjust as needed
    )
    return response.choices[0].text.strip()




class CodeEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.is_dark_theme = False  # Default theme is light

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Code Editor - VSCode Style")

        # Create MenuBar
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

        view_menu = menubar.addMenu("View")
        toggle_theme_action = QAction("Toggle Dark Theme", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # File Navigation Sidebar
        self.file_nav = QDockWidget("File Navigation", self)
        self.file_tree = QTreeView()
        self.file_tree.clicked.connect(self.open_selected_file)
        self.file_nav.setWidget(self.file_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.file_nav)

        # Terminal
        self.terminal = QDockWidget("Terminal", self)
        self.terminal_widget = QTextEdit()
        self.terminal_widget.setReadOnly(True)
        self.terminal_input = QLineEdit()
        self.terminal_input.returnPressed.connect(self.execute_command)

        self.terminal_layout = QVBoxLayout()
        self.terminal_layout.addWidget(self.terminal_widget)
        self.terminal_layout.addWidget(self.terminal_input)

        terminal_widget_container = QWidget()
        terminal_widget_container.setLayout(self.terminal_layout)
        self.terminal.setWidget(terminal_widget_container)

        self.addDockWidget(Qt.BottomDockWidgetArea, self.terminal)

        # Code Editor
        self.code_editor = QPlainTextEdit()
        self.layout.addWidget(self.code_editor)

        self.central_widget.setLayout(self.layout)

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.populate_file_tree(folder_path)

    def populate_file_tree(self, folder_path):
        model = QFileSystemModel()
        model.setRootPath(folder_path)
        self.file_tree.setModel(model)
        self.file_tree.setRootIndex(model.index(folder_path))

    def open_selected_file(self, index):
        selected_file = self.file_tree.model().filePath(index)
        with open(selected_file, 'r') as file:
            self.code_editor.setPlainText(file.read())

    def execute_command(self):
        command = self.terminal_input.text()
        self.terminal_widget.append(f"> {command}")
        # You can implement command execution here and append the output to the terminal

        self.terminal_input.clear()

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            self.setStyleSheet("background-color: #222; color: #FFF;")
        else:
            self.setStyleSheet("background-color: #FFF; color: #000;")

    def stream_gpt_response(self, prompt):
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        stream=True
    )
        for chunk in response:
            print(chunk.choices)
            if isinstance(chunk, dict) and 'text' in chunk:
                print(chunk)
                self.terminal_widget.append(chunk['text'])



    def execute_command(self):
        command = self.terminal_input.text()

        if command.startswith("gpt:"):
            gpt_input = command[len("gpt:"):]
            self.stream_gpt_response(gpt_input)
        else:
            self.terminal_widget.append(f"> {command}")
            # You can implement command execution here and append the output to the terminal

        self.terminal_input.clear()

def main():
    app = QApplication(sys.argv)
    window = CodeEditor()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()