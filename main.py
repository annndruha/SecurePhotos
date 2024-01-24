import sys
from PyQt5 import QtWidgets
from src.window_app import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    application = MainWindow()
    application.show()
    app.exec()
