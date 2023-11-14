import sys
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QIcon, QPixmap, QGuiApplication
from PySide6.QtCore import Qt, QTimer

from windows.user_journey_window import UserJourneyWindow

def main():
    app = QApplication(sys.argv)
    # Dark Theme
    app.setStyle("Fusion")
    # Light Theme
    # app.setStyle("Breeze")

    # app.setStyle("GTK+")

    app.setWindowIcon(QIcon("./ACELogo.png"))

    # Create a QPixmap object with the image you want to show
    splash_pix = QPixmap('./ACELogo.png')

    # Scale QPixmap to desired size
    splash_pix = splash_pix.scaled(400, 400, Qt.KeepAspectRatio)

    # Create a QSplashScreen object and pass the QPixmap object to it
    splash = QSplashScreen(splash_pix)
    
    # Center the splash screen on the display
    screen_geometry = QGuiApplication.primaryScreen().geometry()
    splash_geometry = splash.geometry()
    x = (screen_geometry.width() - splash_geometry.width()) / 2
    y = (screen_geometry.height() - splash_geometry.height()) / 2
    splash.move(x, y)

    splash.show()

    # Hide the splash screen after 3 seconds (3000 milliseconds)
    QTimer.singleShot(3000, splash.close)

    user_journey_window = UserJourneyWindow()
    user_journey_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()