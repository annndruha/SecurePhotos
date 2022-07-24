# import os
# import sys
#
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtQml import QQmlApplicationEngine
# from PySide6.QtQuickControls2 import QQuickStyle
#
# if __name__ == "__main__":
#     QQuickStyle.setStyle("Material")
#
#     app = QGuiApplication(sys.argv)
#     engine = QQmlApplicationEngine()
#     engine.load(os.path.join(os.path.dirname(__file__), "Design.qml"))
#     if not engine.rootObjects():
#         sys.exit(-1)
#     sys.exit(app.exec_())
#
#
import os
from aes.aes import encrypt_file, decrypt_file

keyphrase = 'mypassword'
encrypt_file(os.path.join('space.jpg'), keyphrase)
decrypt_file(os.path.join('space.jpg.aes'), keyphrase)
#
# import sys
# from pathlib import Path
#
# from PySide6.QtCore import QObject, Slot
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtQml import QQmlApplicationEngine, QmlElement
# from PySide6.QtQuickControls2 import QQuickStyle
#
# # import style_rc
#
# # To be used on the @QmlElement decorator
# # (QML_IMPORT_MINOR_VERSION is optional)
# QML_IMPORT_NAME = "io.qt.textproperties"
# QML_IMPORT_MAJOR_VERSION = 1
#
#
# @QmlElement
# class Bridge(QObject):
#
#     @Slot(str, result=str)
#     def getColor(self, s):
#         if s.lower() == "red":
#             return "#ef9a9a"
#         elif s.lower() == "green":
#             return "#a5d6a7"
#         elif s.lower() == "blue":
#             return "#90caf9"
#         else:
#             return "white"
#
#     @Slot(float, result=int)
#     def getSize(self, s):
#         size = int(s * 34)
#         if size <= 0:
#             return 1
#         else:
#             return size
#
#     @Slot(str, result=bool)
#     def getItalic(self, s):
#         if s.lower() == "italic":
#             return True
#         else:
#             return False
#
#     @Slot(str, result=bool)
#     def getBold(self, s):
#         if s.lower() == "bold":
#             return True
#         else:
#             return False
#
#     @Slot(str, result=bool)
#     def getUnderline(self, s):
#         if s.lower() == "underline":
#             return True
#         else:
#             return False
#
#
# if __name__ == '__main__':
#     app = QGuiApplication(sys.argv)
#     QQuickStyle.setStyle("Material")
#     engine = QQmlApplicationEngine()
#
#     # Get the path of the current directory, and then add the name
#     # of the QML file, to load it.
#     qml_file = Path(__file__).parent / 'Design.qml'
#     engine.load(qml_file)
#
#     if not engine.rootObjects():
#         print('QML Error')
#         sys.exit(-1)
#
#     sys.exit(app.exec())

