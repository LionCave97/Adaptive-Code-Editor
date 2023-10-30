import pyperclip
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QProcess
import os
import sys
import subprocess
from git import Repo, InvalidGitRepositoryError
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

        self.is_dark_theme = True
                
       

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

        new_file_action = QAction("New File", self)
        new_file_action.triggered.connect(self.create_new_file)
        file_menu.addAction(new_file_action)

        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        # Add 'Restart' action
        restart_action = QAction("Restart", self)
        restart_action.triggered.connect(self.restart_app)
        file_menu.addAction(restart_action)

        # Add 'Close' action
        close_action = QAction("Close", self)
        close_action.triggered.connect(self.close)
        file_menu.addAction(close_action)

        view_menu = menubar.addMenu("View")
        toggle_theme_action = QAction("Toggle Theme", self)
        toggle_theme_action.triggered.connect(self.toggle_theme)
        view_menu.addAction(toggle_theme_action)

        clear_terminal_action = QAction("Clear Terminal", self)
        clear_terminal_action.triggered.connect(self.clear_terminal)
        view_menu.addAction(clear_terminal_action)

        templates_menu = menubar.addMenu("Workspace")

        beginner_template_action = QAction("Basic", self)
        beginner_template_action.triggered.connect(self.load_beginner_template)
        templates_menu.addAction(beginner_template_action)

        # moderate_template_action = QAction("Moderate", self)
        # moderate_template_action.triggered.connect(self.load_moderate_template)
        # templates_menu.addAction(moderate_template_action)

        advanced_template_action = QAction("Advanced", self)
        advanced_template_action.triggered.connect(self.load_advanced_template)
        templates_menu.addAction(advanced_template_action)

        templates_menu = menubar.addMenu("Tools")

        # Add 'Lint Code' action
        lint_action = QAction("Lint Code", self)
        lint_action.triggered.connect(self.lint_code)
        templates_menu.addAction(lint_action)


        

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

        self.git_widget = QDockWidget("Git", self)
        self.git_status = QTextEdit()
        self.git_status.setReadOnly(True)
        self.git_widget.setWidget(self.git_status)
        self.git_widget.hide()

        
        self.addDockWidget(Qt.BottomDockWidgetArea, self.git_widget)

        self.pylint_widget = QDockWidget("Debug", self)
        self.pylint_output = QTextEdit()
        self.pylint_output.setReadOnly(True)
        self.pylint_widget.setWidget(self.pylint_output)
        self.pylint_widget.hide()

        self.addDockWidget(Qt.BottomDockWidgetArea, self.pylint_widget)


        # Code Editor
        
        self.code_editor = QPlainTextEdit()
        highlighter = HTMLHighlighter(self.code_editor.document())
        highlighter = PythonHighlighter(self.code_editor.document())
        self.code_editor.textChanged.connect(self.save_file)


        self.layout.addWidget(self.code_editor)

        self.central_widget.setLayout(self.layout)

        # Get started message in terminal.
        self.terminal_widget.append("Hello, this is your terminal area. You can use this to chat with a assistant.")

        self.terminal_widget.append("You can just type to ask questions and use 'code:' to generate and debug code. You can also use 'help' for basic commands.")

        self.open_terminal_button = QPushButton("Run Code", self)
        self.open_terminal_button.clicked.connect(self.open_terminal_at_path)
        self.layout.addWidget(self.open_terminal_button)
        self.open_terminal_button.hide()

       
        # ...
        self.process = None

        self.dockable_widgets = {
            "File Navigation": self.file_nav,
            "Terminal": self.terminal,
            "Git": self.git_widget,
            "Linter": self.pylint_widget,            
        }
        
        def create_toggle_action(widget):
            return lambda checked: widget.setVisible(checked)

        dockable_menu = menubar.addMenu("Panels")
        for name, widget in self.dockable_widgets.items():
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(True)
            action.triggered.connect(create_toggle_action(widget))
            dockable_menu.addAction(action)

    def update_git_status(self):
        try:
            repo = Repo(self.project_directory)
            self.git_status.setText(repo.git.status())
        except InvalidGitRepositoryError:
            self.git_status.setText("Not a Git repository")

    
    def lint_code(self):
        # Get the currently selected file
        selected_index = self.file_tree.currentIndex()
        selected_file = self.file_tree.model().filePath(selected_index)
        self.pylint_output.setText("")
        # Run pylint on the file
        try:
            result = subprocess.run(['python', '-m', 'pylint', selected_file], capture_output=True, text=True)
            # Display the results in the terminal
            self.pylint_output.append(result.stdout)
        except FileNotFoundError:
            self.pylint_output.append("pylint is not installed or not found in PATH")

    def create_new_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "New File", "", "All Files (*)")
        if file_path:
            with open(file_path, 'w') as file:
                pass  # Create an empty file
            self.populate_file_tree(os.path.dirname(file_path))

    def restart_app(self):
        QApplication.quit()
        subprocess.run([sys.executable] + sys.argv, cwd=sys.path[0])

    def open_terminal_at_path(self):
    # If a process is already running, terminate it
        if self.process is not None:
            self.process.kill()
            self.process = None
            self.open_terminal_button.setText("Open Terminal")
            return

        selected_index = self.file_tree.currentIndex()
        selected_file = self.file_tree.model().filePath(selected_index)
        directory = os.path.dirname(selected_file)
        file_name = os.path.basename(selected_file)

        if file_name.endswith('.py'):
            self.process = subprocess.Popen('start cmd /k python {}'.format(file_name), cwd=directory, shell=True)
        elif file_name.endswith('.html'):
            self.process = subprocess.Popen('start cmd /k live-server', cwd=directory, shell=True)
        else:
            self.process = subprocess.Popen('start cmd', cwd=directory, shell=True)

        self.open_terminal_button.setText("Stop Terminal")

    def load_beginner_template(self):
        # Load the beginner template into the code editor
        # self.code_editor.setPlainText("Beginner workspace...")
        self.file_nav.show()  # Show the file navigation
        self.git_widget.hide()
        self.pylint_widget.hide()


        self.terminal.show()  # Show the terminal
        # Hide any advanced features
        for widget in self.dockable_widgets.values():
            if widget not in [self.file_nav, self.terminal]:
                widget.hide()

    def load_moderate_template(self):
        # Load the moderate template into the code editor
        # self.code_editor.setPlainText("Moderate workspace...")
        print("Moderate workspace...")

    def load_advanced_template(self):
        # Load the advanced template into the code editor
        # self.code_editor.setPlainText("Advanced workspace...")
        # Show all dockable widgets
        for widget in self.dockable_widgets.values():
            widget.show()
    
    def clear_terminal(self):
        self.terminal_widget.clear()

    def open_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.populate_file_tree(folder_path)

        # Set the project_directory attribute
        self.project_directory = folder_path
        self.update_git_status()
        

    def populate_file_tree(self, folder_path):
        model = QFileSystemModel()
        model.setRootPath(folder_path)
        self.file_tree.setModel(model)
        self.file_tree.setRootIndex(model.index(folder_path))

    def open_selected_file(self, index):
        selected_file = self.file_tree.model().filePath(index)
        file_extension = os.path.splitext(selected_file)[1]

        # Show the button if the file is a .py or .html file
        if file_extension in ['.py', '.html']:
            self.open_terminal_button.show()
        else:
            self.open_terminal_button.hide()

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

        # Update Git status when file changes happen
        self.update_git_status()



    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme
        print("toggle theme")
        if self.is_dark_theme:
            print("dark")
            QApplication.instance().setStyle("Fusion")
        else:
            # self.setStyleSheet("background-color: #FFF; color: #000;")
            print("light")
            QApplication.instance().setStyle("GTK+")
            
    def gpt_response(self, prompt):
        # Get the currently selected file
        selected_index = self.file_tree.currentIndex()
        selected_file = self.file_tree.model().filePath(selected_index)

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

        if command.startswith("code:"):
            self.terminal_widget.append("Please wait. I am generating the code")
            gpt_input = command[len("ask:"):]
            self.gpt_response(command)
            
        elif command.startswith("help"):
            self.terminal_widget.append("You can just type to ask questions.")
            self.terminal_widget.append("Use 'code:' to generate and debug code.")
            self.terminal_widget.append("Use 'clear:' to clear the terminal.")
            self.terminal_widget.append(" You can also use 'help' for basic commands.")

        elif command.startswith("clear"):
            self.terminal_widget.setText("")
        else:
            self.stream_gpt_response(command)
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