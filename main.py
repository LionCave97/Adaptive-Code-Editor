import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QDockWidget, QTreeView, QTextEdit, QLineEdit, QFileDialog, QMenuBar, QPushButton, QFileSystemModel
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtCore import Qt, QDir

from highlighter.pyhiglighter import PythonHighlighter
from highlighter.htmlhighlighter import HTMLHighlighter

from code_gen import code_gen

import openai


def get_gpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Choose an appropriate engine
        prompt=prompt,
        max_tokens=8000  # Adjust as needed
    )
    return response.choices[0].text.strip()


class UserJourneyWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("User Journey - Code Editor Setup")
        self.setGeometry(100, 100, 800, 600)
        self.set_dark_mode()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.chat_widget = QTextEdit()
        self.chat_widget.setReadOnly(True)
        layout.addWidget(self.chat_widget)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.clicked.connect(self.proceed_user_journey)
        layout.addWidget(self.proceed_button)
        self.chat_history = []
        central_widget.setLayout(layout)

        self.setup_user_journey()

    def setup_user_journey(self):
        self.user_journey = [
            ("Welcome to the Code Editor!", "How can I assist you today?\n1. Open a folder\n2. Set up a new project"),
            ("Select an option:", "1. Open a folder\n2. Set up a new project"),
            ("Open a Folder", "Please select the folder you want to open."),
            ("Set Up New Project", "Let's set up a new project! What's the project name?"),
            # ... Add more steps as needed
        ]
        self.current_journey_step = 0

        # self.update_chat_widget()

    def proceed_user_journey(self):
        if self.current_journey_step < len(self.user_journey):
            _, response = self.user_journey[self.current_journey_step]
            input_text = self.input_field.text()  # Get user input
            self.chat_history.append(f"> You: {input_text}")
            self.chat_history.append(f"> Assistant: {response}")
            self.current_journey_step += 1
            self.update_chat_widget()

            if self.current_journey_step == len(self.user_journey):
                self.user_journey_completed()
                self.open_code_editor(input_text)  

    def open_code_editor(self, project_name):
        self.close()  # Close the user journey window
        self.code_editor_window = CodeEditor(project_name)
        self.code_editor_window.show()
        
    def next_step(self):
        self.current_step += 1
        if self.current_step < len(self.steps):
            assistant_response = self.get_gpt_response(self.steps[self.current_step][1])
            self.steps[self.current_step] = (self.steps[self.current_step][0], assistant_response)
            self.text_widget.setPlainText(assistant_response)
            self.next_button.setText("Next")
        else:
            self.close()  # Close the user journey window
            self.open_main_code_editor()

    def get_gpt_response(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()

    def open_main_code_editor(self):
        self.main_code_editor = CodeEditor()
        self.main_code_editor.show()

    def set_dark_mode(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QDockWidget {
                background-color: #252526;
                color: #d4d4d4;
                border: 1px solid #181818;
            }
            QTreeView {
                background-color: #252526;
                color: #d4d4d4;
                border: none;
            }
            QTextEdit, QPlainTextEdit, QLineEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #181818;
                selection-color: #ffffff;
                selection-background-color: #264f78;
            }
            QMenuBar {
                background-color: #333;
                color: #ffffff;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 10px;
            }
            QMenuBar::item:selected {
                background-color: #555;
            }
            QMenu {
                background-color: #333;
                color: #ffffff;
            }
            QMenu::item {
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #555;
            }
            QTreeView::item {
                border: none;
            }
        """)



class CodeEditor(QMainWindow):

    def __init__(self):
        super().__init__()

        self.is_dark_theme = True
        self.set_dark_theme()

        self.init_ui()
        

        self.setup_user_journey()

    def update_chat_widget(self):
        self.chat_widget.setPlainText("\n".join(self.chat_history))

    

    def proceed_user_journey(self, input_text):
        if self.current_journey_step < len(self.user_journey):
            _, response = self.user_journey[self.current_journey_step]
            self.chat_history.append(f"> You: {input_text}")
            self.chat_history.append(f"> Assistant: {response}")
            self.current_journey_step += 1
            self.update_chat_widget()

            if self.current_journey_step == len(self.user_journey):
                self.user_journey_completed()

    def user_journey_completed(self):
        self.chat_history.append("> Assistant: User journey completed!")
        self.update_chat_widget()

    # ...

    def execute_command(self):
        command = self.terminal_input.text()

        if command.startswith("gpt:"):
            gpt_input = command[len("gpt:"):]
            self.stream_gpt_response(gpt_input)
            self.proceed_user_journey(gpt_input)  # Add this line to integrate user journey
        else:
            self.terminal_widget.append(f"> {command}")
            # You can implement command execution here and append the output to the terminal

        self.terminal_input.clear()


    def init_ui(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Code Editor - VSCode Style")

        # Create MenuBar
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        view_menu = menubar.addMenu("View")
        toggle_theme_action = QAction("Toggle Dark Theme", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)

        clear_terminal_action = QAction("Clear Terminal", self)
        clear_terminal_action.triggered.connect(self.clear_terminal)
        view_menu.addAction(clear_terminal_action)

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
        highlighter = HTMLHighlighter(self.code_editor.document())
        highlighter = PythonHighlighter(self.code_editor.document())

        self.layout.addWidget(self.code_editor)

        self.central_widget.setLayout(self.layout)

        self.chat_history = []
        # Chat Window
        self.chat_widget = QTextEdit()
        self.chat_widget.setReadOnly(True)
        self.layout.addWidget(self.chat_widget)
    
    def clear_terminal(self):
        self.terminal_widget.clear()

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
    
    def save_file(self):
        selected_index = self.file_tree.currentIndex()
        selected_file = self.file_tree.model().filePath(selected_index)
        
        if not selected_file:
            return
        
        with open(selected_file, 'w') as file:
            file.write(self.code_editor.toPlainText())



    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        if self.is_dark_theme:
            # self.setStyleSheet("background-color: #222; color: #FFF;")
            self.set_dark_theme()
        else:
            self.setStyleSheet("background-color: #FFF; color: #000;")
    
    def set_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QDockWidget {
                background-color: #252526;
                color: #d4d4d4;
                border: 1px solid #181818;
            }
            QTreeView {
                background-color: #252526;
                color: #d4d4d4;
                border: none;
            }
            QTextEdit, QPlainTextEdit, QLineEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #181818;
                selection-color: #ffffff;
                selection-background-color: #264f78;
            }
            QMenuBar {
                background-color: #333;
                color: #ffffff;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 10px;
            }
            QMenuBar::item:selected {
                background-color: #555;
            }
            QMenu {
                background-color: #333;
                color: #ffffff;
            }
            QMenu::item {
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #555;
            }
            QTreeView::item {
                border: none;
            }
        """)

    def stream_gpt_response(self, prompt):
        response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        stream=True
    )
        concatenated_text = ""
        for chunk in response:
            print(chunk.choices[0].text)
            if isinstance(chunk, dict) and 'text' in chunk.choices[0]:
                concatenated_text += chunk.choices[0].text
                self.terminal_widget.setPlainText(concatenated_text)



    def execute_command(self):
        command = self.terminal_input.text()

        if command.startswith("gpt:"):
            gpt_input = command[len("gpt:"):]
            self.stream_gpt_response(gpt_input)

        elif command.startswith("code:"):
            gpt_input = command[len("code:"):]
            self.generate_code(gpt_input)
        else:
            self.terminal_widget.append(f"> {command}")
            # You can implement command execution here and append the output to the terminal

        self.terminal_input.clear()

    def generate_code(self, gpt_input):
        # print("Prompt Input", self.codePromptInput.toPlainText())
        QApplication.processEvents()
        code = code_gen.generate_code(gpt_input, "html")
        self.terminal_widget.append(code)
        # print(code)
        # self.editor.setPlainText(code)
       

    def add_code(self):
        # print("Prompt Input", self.codePromptInput.toPlainText())
        QApplication.processEvents()
        code = code_gen.add_code(self.codePromptInput.toPlainText(),self.editor.toPlainText(),  "html")
        print(code)
        return code

     


def main():
    app = QApplication(sys.argv)

    user_journey_window = UserJourneyWindow()
    user_journey_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()