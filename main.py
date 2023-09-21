import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget, QDockWidget, QTreeView, QTextEdit, QLineEdit, QFileDialog, QMenuBar, QPushButton, QFileSystemModel
from PySide6.QtGui import QPalette, QColor, QAction
from PySide6.QtCore import Qt, QDir

from highlighter.pyhiglighter import PythonHighlighter
from highlighter.htmlhighlighter import HTMLHighlighter

from code_gen.code_gen import code_gen

import openai

from windows.user_journey_window import UserJourneyWindow
from windows.code_editor import CodeEditor



     


def main():
    app = QApplication(sys.argv)

    user_journey_window = UserJourneyWindow()
    user_journey_window.show()

    # window = CodeEditor(user_journey_window)
    # window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()