from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QLabel
from PySide6.QtCore import Qt, Signal

from windows.code_editor import CodeEditor
from code_gen.code_gen import code_gen

from windows.code_editor import CodeEditor

class UserJourneyWindow(QMainWindow):
    code_generated = Signal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.code_editor = None  # Add this line


    def init_ui(self):
        self.central_widget = QWidget()  # Create a central widget
        self.setCentralWidget(self.central_widget)  # Set the central widget

        self.layout = QVBoxLayout(self.central_widget)  # Add the layout to the central widget


        self.project_goals_input = QLineEdit()
        self.layout.addWidget(QLabel("What are your project goals?"))
        self.layout.addWidget(self.project_goals_input)

        self.layout.addWidget(QLabel("Which Languages will you use?"))
        self.language_group = QButtonGroup()
        self.languages = ["Python", "React", "HTML/CSS/JS"]
        for language in self.languages:
            btn = QRadioButton(language)
            self.language_group.addButton(btn)
            self.layout.addWidget(btn)

        self.project_scope_input = QLineEdit()
        self.layout.addWidget(QLabel("Briefly describe the project Scope"))
        self.layout.addWidget(self.project_scope_input)

        self.layout.addWidget(QLabel("What is your skill level:"))
        self.skill_level_group = QButtonGroup()
        for i in range(1, 6):
            btn = QRadioButton(str(i))
            self.skill_level_group.addButton(btn)
            self.layout.addWidget(btn)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def submit(self):
        project_goals = self.project_goals_input.text()
        language = self.languages[self.language_group.checkedId()]
        project_scope = self.project_scope_input.text()
        skill_level = self.skill_level_group.checkedId()

        generated_code = code_gen.generate_code(project_goals, language, project_scope, skill_level)

        # Handle the generated code
        # For example, you can print it to the console for now
        print(generated_code)

        # Pass these values to the code generator
        # code_gen.generate_code(project_goals, language, project_scope, skill_level)
        generated_code_path = code_gen.generate_code(project_goals, language, project_scope, skill_level)

        # Create an instance of the CodeEditor class and pass the path of the generated code
        self.code_editor = CodeEditor(self, generated_code_path)
        self.code_editor.show()
        self.close()
        