from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QBrush, QColor


class ZoomQGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super(ZoomQGraphicsView, self).__init__(parent)
        self.verticalScrollBar().hide()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        old_pos = self.mapToScene(event.pos())
        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
        self.scale(zoom_factor, zoom_factor)
        new_pos = self.mapToScene(event.pos())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())


class FullScreen(ZoomQGraphicsView):
    escapeSignal = QtCore.pyqtSignal()
    nextSignal = QtCore.pyqtSignal()
    prevSignal = QtCore.pyqtSignal()

    def __init__(self):
        super(FullScreen, self).__init__()
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.FramelessWindowHint)
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
        border = 1
        screen_size = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.move(-border, -border)
        self.resize(QSize(screen_size.width() + 2*border, screen_size.height() + 2*border))
        self.fitInView(self.scene().itemsBoundingRect(), Qt.KeepAspectRatio)
