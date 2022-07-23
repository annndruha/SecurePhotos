import os
import sys

from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # style = QStyleFactory.create("Fusion")  # ['windowsvista', 'Windows', 'Fusion']
    # print(style)
    # # app.setStyle(style)
    # app.setStyle(style)

    ui_file = QFile("mainwindow.ui")
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()
    sys.exit(app.exec())


# import os
# from encrypt_code.image_engine import encrypt_image, decrypt_image
#
# keyphrase = 'mypassword'
# encrypt_image(os.path.join('space.jpg'), keyphrase)
# decrypt_image(os.path.join('space.cipher'), keyphrase)
