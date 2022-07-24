from PyQt5 import QtWidgets
from src.mainwindow import MainWindow


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()
    app.exec()
