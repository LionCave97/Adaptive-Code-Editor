from PySide6.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QProgressDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QRadioButton, QButtonGroup, QLabel
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
        self.layout.addWidget(QLabel("What is the goal of the project?"))
        self.layout.addWidget(self.project_goals_input)

        self.layout.addWidget(QLabel("What is the preferred method of development?"))
        self.language_group = QButtonGroup()
        self.languages = ["Python", "HTML"]
        language_layout = QHBoxLayout()
        for i, language in enumerate(self.languages):
            btn = QRadioButton(language)
            self.language_group.addButton(btn, i)  # Assign id to the button
            language_layout.addWidget(btn)
        self.layout.addLayout(language_layout)

        self.layout.addWidget(QLabel("What is your skill level?"))
        self.skill_level_group = QButtonGroup()
        self.skill_levels = ["Beginner", "Intermediate", "Expert"]
        skill_level_layout = QHBoxLayout()
        for i, skill_level in enumerate(self.skill_levels):
            btn = QRadioButton(skill_level)
            self.skill_level_group.addButton(btn, i)
            skill_level_layout.addWidget(btn)
        self.layout.addLayout(skill_level_layout)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #333;
                color: #fff;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QPushButton:pressed {
                background-color: #999;
            }
        """)
        self.layout.addWidget(self.submit_button)

        self.open_editor_button = QPushButton("Open Editor")
        self.open_editor_button.clicked.connect(self.open_editor)
        self.layout.addWidget(self.open_editor_button)


        self.setLayout(self.layout)

    def open_editor(self):
        # Create an instance of the CodeEditor class
        self.code_editor = CodeEditor(self)
        self.code_editor.show()    
        self.close()


    def submit(self):
        project_goals = self.project_goals_input.text()
        language_id = self.language_group.checkedId()
        language = self.languages[language_id]
        project_scope = self.project_goals_input.text()
        skill_level = self.skill_level_group.checkedId()

        if not project_goals or language_id == -1 or skill_level == -1:
            QMessageBox.warning(self, "Missing Data", "Please fill in all fields.")
            return
        
        progress = QProgressDialog("Generating code...", "Cancel", 0, 0, self)
        progress.setWindowModality(Qt.WindowModal)
        progress.setMaximum(0)  # Add this line
        progress.show()

        QApplication.processEvents()  # Add this line

        generated_code_path = code_gen.generate_new_code(project_goals, language, project_scope, skill_level)

        progress.close()

        if isinstance(generated_code_path, list):
            # If multiple files are generated, open the first one by default
            self.code_editor = CodeEditor(self, generated_code_path[0])
        else:
            self.code_editor = CodeEditor(self, generated_code_path)


        # Create an instance of the CodeEditor class and pass the path of the generated code
        self.code_editor = CodeEditor(self, generated_code_path)
        self.code_editor.show()
        self.close()
        