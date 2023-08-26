from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton
from PySide6.QtCore import Qt

from windows.code_editor import CodeEditor

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

        central_widget.setLayout(layout)

        self.setup_user_journey()

    def setup_user_journey(self):
        self.user_journey = [
            ("Project Goals", "What are your project goals?"),
            ("Tech Stack", "Which technologies will you use?"),
            ("Scope", "Briefly describe the project's scope."),
            ("Challenges", "Are there any anticipated challenges?"),
            ("Skill Level", "On a scale of 1 to 5, how would you rate your development skills (1 being beginner, 5 being expert)?"),
        ]
        self.current_journey_step = 0
        self.display_next_question()

    def display_next_question(self):
        if self.current_journey_step < len(self.user_journey):
            _, step_question = self.user_journey[self.current_journey_step]
            self.chat_widget.append(f"> Assistant: {step_question}")

    def proceed_user_journey(self):
        if self.current_journey_step < len(self.user_journey):
            input_text = self.input_field.text()  # Get user input
            self.chat_widget.append(f"> You: {input_text}")
            self.current_journey_step += 1
            self.input_field.clear()
            self.display_next_question()

            if self.current_journey_step == len(self.user_journey):
                self.open_code_editor()


    def update_chat_widget(self):
        # Clear and update the chat_widget with chat_history
        self.chat_widget.clear()
        self.chat_widget.append("\n".join(self.chat_history))

    # ... Other methods


    def open_code_editor(self):
        # project_name = self.responses.get("Set Up New Project", "MyProject")  # Get project name (default to "MyProject")
        # project_goals = self.responses.get("Project Goals", "")
        # tech_stack = self.responses.get("Tech Stack", "")
        # scope = self.responses.get("Scope", "")
        # challenges = self.responses.get("Challenges", "")
        # skill_level = self.responses.get("Skill Level", "")

        # # Pass the collected information to your CodeEditor class and set up the UI
        # self.code_editor_window = CodeEditor()
        # self.code_editor_window.generate_code_and_setup_ui(project_name, project_goals, tech_stack, scope, challenges, skill_level)
        window = CodeEditor()
        window.show()
        self.close()  # Close the user journey window


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
