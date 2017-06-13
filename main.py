# Import Python modules
import sys

# Import Qt modules
from PyQt5.QtWidgets import QMainWindow, QApplication

# Import the compiled UI module
from mainwindow import Ui_MainWindow


# Create a class for the main window
class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Setup the ui form
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Show the GraphicsViews
        self.ui.graphicsView.show()

        # Connect Actions
        # File menu
        self.ui.actionClose.triggered.connect(self.close)


def main():
    # Show our mainwindow
    app = QApplication(sys.argv)
    labyrinth = Main()
    labyrinth.show()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
