# import sys
# import os
#
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtUiTools import QUiLoader
# from PySide6.QtQml import QQmlApplicationEngine
# from PySide6.QtCore import QFile, QIODevice
# from PySide6.QtQuickControls2 import QQuickStyle
#
# import rc_main
#
# if __name__ == "__main__":
#
#     # How to set the style for QtQuick :
#
#     # Option 1 - passing or forcing --style argument
#     # sys.argv += ['--style', 'material']
#
#     # Option 2 - use QtQuickStyle module
#     if not os.environ.get("QT_QUICK_CONTROLS_STYLE"):
#         QQuickStyle.setStyle("Material")
#
#     app = QGuiApplication(sys.argv)
#     # engine = QQmlApplicationEngine()
#     # engine.load(os.path.join(os.path.dirname(__file__), "DesignForm.ui.qml"))
#     # if not engine.rootObjects():
#     #     sys.exit(-1)
#
#     ui_file_name = "mainwindow.ui"
#     ui_file = QFile(ui_file_name)
#     if not ui_file.open(QIODevice.ReadOnly):
#         print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
#         sys.exit(-1)
#     loader = QUiLoader()
#     window = loader.load(ui_file)
#     ui_file.close()
#     if not window:
#         print(loader.errorString())
#         sys.exit(-1)
#     window.show()
#     sys.exit(app.exec_())




































# import os
# from encrypt_code.image_engine import encrypt_image, decrypt_image
#
# keyphrase = 'mypassword'
# encrypt_image(os.path.join('space.jpg'), keyphrase)
# decrypt_image(os.path.join('space.cipher'), keyphrase)

import sys
import os
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtCore import QFile, QIODevice

if __name__ == "__main__":
    app = QApplication(sys.argv)
    style = QStyleFactory.create("Fusion")  # ['windowsvista', 'Windows', 'Fusion']
    print(style)
    # app.setStyle(style)
    app.setStyle(style)

    ui_file = QFile("mainwindow.ui")
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    window.show()
    sys.exit(app.exec())
