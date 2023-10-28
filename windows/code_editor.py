import pyperclip
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QProcess

import sys
from PySide6.QtWidgets import QApplication, QMessageBox, QPlainTextEdit, QDockWidget, QTreeView, QFileDialog, QMenuBar, QPushButton, QFileSystemModel
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtCore import Qt, QDir

import openai

from highlighter.pyhiglighter import PythonHighlighter
from highlighter.htmlhighlighter import HTMLHighlighter

from code_gen.code_gen import code_gen

class CodeEditor(QMainWindow):

    def __init__(self, user_journey_window, folder_path=None):
        super().__init__()

        self.user_journey_window = user_journey_window

        self.is_dark_theme = False

        self.init_ui()
        
        # Open the file and set its content to the code editor
        if folder_path is not None:
            self.populate_file_tree(folder_path)

        

    def collect_user_input(self):
        # Get the user input from the UserJourneyWindow
        project_goals = self.user_journey_window.project_goals
        language = self.user_journey_window.language
        project_scope = self.user_journey_window.project_scope
        skill_level = self.user_journey_window.skill_level

        # Return a dictionary of the user input
        return {
            "project_goals": project_goals,
            "language": language,
            "project_scope": project_scope,
            "skill_level": skill_level,
        }
        
    def generate_code_and_setup_ui(self):
        user_input = self.collect_user_input()

        project_name = user_input["project_goals"]
        project_goals = user_input["project_goals"]
        tech_stack = user_input["language"]
        scope = user_input["project_scope"]
        challenges = ""  # You can modify this as needed
        skill_level = user_input["skill_level"]

        generated_code = self.generate_code(user_input)
        self.setup_ui_elements(generated_code)

    def generate_code(self, user_input):
        # Access other required parameters from instance variables
        project_name = self.project_name
        project_goals = self.project_goals
        tech_stack = self.tech_stack
        scope = self.scope
        challenges = self.challenges
        skill_level = self.skill_level

    def setup_ui_elements(self, generated_code):
        # Set up UI elements based on the generated code
        # Finally, you can display the generated code in your code editor
        self.code_editor.setPlainText(generated_code)
        # self.setup_user_journey()

    def update_chat_widget(self):
        self.chat_widget.setPlainText("\n".join(self.chat_history))

    def collect_user_input(self):
        # Implement a method to collect user input or use a stored user response
        # For example, you can return a sample user input for testing purposes
        return "Sample user input"

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

        templates_menu = menubar.addMenu("Templates")

        beginner_template_action = QAction("Beginner Template", self)
        beginner_template_action.triggered.connect(self.load_beginner_template)
        templates_menu.addAction(beginner_template_action)

        moderate_template_action = QAction("Moderate Template", self)
        moderate_template_action.triggered.connect(self.load_moderate_template)
        templates_menu.addAction(moderate_template_action)

        advanced_template_action = QAction("Advanced Template", self)
        advanced_template_action.triggered.connect(self.load_advanced_template)
        templates_menu.addAction(advanced_template_action)




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
        self.terminal_input.setPlaceholderText("Enter your command here... And press 'Enter'")
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
        self.code_editor.textChanged.connect(self.save_file)

        self.layout.addWidget(self.code_editor)

        self.central_widget.setLayout(self.layout)

        # Get started message in terminal.
        self.terminal_widget.append("Hello, this is your terminal area. You can use this to chat with a assistant.")

        self.terminal_widget.append("Use 'gpt:' to ask a question and use 'code:' to generate new code.")


    def load_beginner_template(self):
        # Load the beginner template into the code editor
        self.code_editor.setPlainText("Beginner template code...")
        self.file_nav.hide()

    def load_moderate_template(self):
        # Load the moderate template into the code editor
        self.code_editor.setPlainText("Moderate template code...")

    def load_advanced_template(self):
        # Load the advanced template into the code editor
        self.code_editor.setPlainText("Advanced template code...")
    
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
        print("toggle theme")
        if self.is_dark_theme:
            print("dark")
            QApplication.instance().setStyle("Fusion")

        else:
            # self.setStyleSheet("background-color: #FFF; color: #000;")
            print("light")
            QApplication.instance().setStyle("Breeze")


    def gpt_response(self, prompt):
        # Get the currently selected file
        selected_index = self.file_tree.currentIndex()
        selected_file = self.file_tree.model().filePath(selected_index)
        self.terminal_widget.append("Please wait. I am generating the code")

        # Read the contents of the file
        with open(selected_file, 'r') as file:
            file_contents = file.read()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a coding assistant, that only returns code no extra text allowed."},
                {"role": "user", "content": prompt + file_contents}
            ],
            max_tokens=6000,
            stream=False
        )
        print(response['choices'][0]['message']['content'])
        self.terminal_widget.append(response['choices'][0]['message']['content'])


        msg_box = QMessageBox()
        msg_box.setText("Do you want to copy the generated code to the clipboard?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec()

        # If the user clicked 'Yes', copy the generated code to the clipboard
        if result == QMessageBox.Yes:
            pyperclip.copy(response['choices'][0]['message']['content'])

    def stream_gpt_response(self, prompt):
        # Get the currently selected file
        selected_index = self.file_tree.currentIndex()
        selected_file = self.file_tree.model().filePath(selected_index)

        # Read the contents of the file
        with open(selected_file, 'r') as file:
            file_contents = file.read()

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a coding assistant."},
                {"role": "user", "content": prompt + file_contents}
            ],
            max_tokens=6000,
            stream=True
        )
        self.terminal_widget.append("")

        for chunk in response:
            try:
                chunk_content =chunk['choices'][0]['delta']['content']
                self.terminal_widget.insertPlainText(chunk['choices'][0]['delta']['content'])
                QApplication.processEvents()

            except:
                print("An error occurred while streaming the GPT response.")
                pass




    def execute_command(self):
        command = self.terminal_input.text()
        self.terminal_widget.append(f"> {command}")
        self.terminal_input.clear()

        if command.startswith("ask:"):
            gpt_input = command[len("ask:"):]
            self.gpt_response(command)
            
        elif command.startswith("help"):
            self.terminal_widget.append("Use 'gpt:' to ask a question and use 'code:' to generate new code.")
        else:
            self.add_code(command)
        # You can implement command execution here and append the output to the terminal

    def generate_code(self, gpt_input):
        # print("Prompt Input", self.codePromptInput.toPlainText())
        QApplication.processEvents()
        code = code_gen.generate_code(gpt_input, "html")
        self.terminal_widget.append(code)
       
    def add_code(self, gpt_input):
        # print("Prompt Input", self.codePromptInput.toPlainText())
        QApplication.processEvents()

        # Get the currently selected file
        selected_index = self.file_tree.currentIndex()
        selected_file = self.file_tree.model().filePath(selected_index)

        # Read the contents of the file
        with open(selected_file, 'r') as file:
            file_contents = file.read()

        # Pass the contents of the file to the code function
        code = code_gen.code(gpt_input, file_contents)
        self.terminal_widget.append(code)
        # Ask the user if they want to copy the generated code to the clipboard
        msg_box = QMessageBox()
        msg_box.setText("Do you want to copy the generated code to the clipboard?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        result = msg_box.exec()

        # If the user clicked 'Yes', copy the generated code to the clipboard
        if result == QMessageBox.Yes:
            pyperclip.copy(code)