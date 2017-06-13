# Import Qt modules
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QPainterPath
from PyQt5.QtWidgets import QGraphicsItem

ORANGE = QColor(250, 200, 10)


class Sender(QObject):
    """
        Helper class for emit a signal
        Pyqt doesn't support multiply inheritance.
        The Button class cannot inherit QGraphicsRectItem and QObject at the same time
    """
    # Define a new signal
    pressed = pyqtSignal()


class ArrowButton(QGraphicsItem):
    """
    TopArrow button for table manipulation

    """
    def __init__(self, parent=None):
        QGraphicsItem.__init__(self, parent)

        # Create the helper attribute for signaling
        self.sender = Sender()

        # For color change
        self.hover = None

        # Enable the hover event
        self.setAcceptHoverEvents(True)

    def boundingRect(self):
        return QRectF(0, 0, 30, 15)

    def paint(self, painter, option, widget):
        if self.hover:
            painter.setBrush(QColor(ORANGE))
            painter.setPen(QColor(ORANGE))
        else:
            painter.setBrush(QColor(Qt.red))
            painter.setPen(QColor(Qt.red))
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(30, 0)
        path.lineTo(15, 15)
        path.closeSubpath()
        painter.drawPath(path)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        # Emit the signal
        self.sender.pressed.emit()

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        # Change the color
        self.hover = True
        self.update()

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        # Change the color back
        self.hover = False
        self.update()