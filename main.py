import sys
from PySide6.QtWidgets import QApplication

from windows.user_journey_window import UserJourneyWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    user_journey_window = UserJourneyWindow()
    user_journey_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()