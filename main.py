# import os
# from encrypt_code.image_engine import encrypt_image, decrypt_image
#
# keyphrase = 'mypassword'
# encrypt_image(os.path.join('space.jpg'), keyphrase)
# decrypt_image(os.path.join('space.cipher'), keyphrase)

import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtCore import QFile, QIODevice
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # style = QStyleFactory.create("windows")  # Fusion, windows
    # app.setStyle(style)

    # engine = QQmlApplicationEngine()
    # QQuickStyle.setStyle("Material")
    QQuickStyle.setStyle('Material')

    ui_file_name = "mainwindow.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()

    sys.exit(app.exec())