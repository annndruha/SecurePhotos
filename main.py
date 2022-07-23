import os
import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

if __name__ == "__main__":
    QQuickStyle.setStyle("Material")

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(os.path.join(os.path.dirname(__file__), "Design.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec_())


# import os
# from encrypt_code.image_engine import encrypt_image, decrypt_image
#
# keyphrase = 'mypassword'
# encrypt_image(os.path.join('space.jpg'), keyphrase)
# decrypt_image(os.path.join('space.cipher'), keyphrase)
