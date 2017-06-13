# https://github.com/MeLikeyCode/QtGameTutorial

# Import Qt modules
from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtGui import QBrush, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject


class Sender(QObject):
    """
        Helper class for emit a signal
        Pyqt doesn't support multiply inheritance.
        The Button class cannot inherit QGraphicsRectItem and QObject at the same time
    """
    # Define a new signal
    pressed = pyqtSignal()


class Button(QGraphicsRectItem):
    def __init__(self, size, text, parent=None):
        QGraphicsRectItem.__init__(self, parent)

        # Create the helper attribute for signaling
        self.sender = Sender()

        # Draw the rect
        self.setRect(size)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.darkCyan)
        self.setBrush(brush)

        # Draw the text (Add self to QGraphicsTextItem to be draw on the scene)
        self.text = QGraphicsTextItem(text, self)
        x = self.rect().width()/2 - self.text.boundingRect().width()/2
        y = self.rect().height()/2 - self.text.boundingRect().height()/2
        font = QFont()
        font.setBold(True)
        self.text.setFont(font)
        self.text.setPos(x, y)

        # Enable the hover event
        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        # Emit the signal
        self.sender.pressed.emit()

    def hoverEnterEvent(self, QGraphicsSceneHoverEvent):
        # Change the color if the mouse hover
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.cyan)
        self.setBrush(brush)

    def hoverLeaveEvent(self, QGraphicsSceneHoverEvent):
        # Change the color back
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.darkCyan)
        self.setBrush(brush)