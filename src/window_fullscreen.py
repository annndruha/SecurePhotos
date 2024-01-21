from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QBrush, QColor

from src.window_graphicsview import ZoomQGraphicsView


class FullScreen(ZoomQGraphicsView):
    escapeSignal = QtCore.pyqtSignal()
    nextSignal = QtCore.pyqtSignal()
    prevSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(FullScreen, self).__init__()
        self.setBackgroundBrush(QBrush(QColor('black')))
        self.setWindowIcon(QIcon('images/icon.png'))

    def keyPressEvent(self, event):
        if event.key() == 16777216:
            self.escapeSignal.emit()
        elif event.key() == 16777236:
            self.nextSignal.emit()
        elif event.key() == 16777234:
            self.prevSignal.emit()

    def update_image(self):
        self.resize(QSize(1920, 1080))  # TODO: Get screen size
        self.fitInView(self.scene().itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
