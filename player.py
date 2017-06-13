# Import Qt modules
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsItem


class Player(QGraphicsItem):
    """
    Player

    """
    def __init__(self, id):
        QGraphicsItem.__init__(self)
        self.id = id
        self.setFlags(QGraphicsItem.ItemSendsGeometryChanges)
        self.locked = True
        self.current_coordinate = ''
        self.cards = []

    def id(self):
        return self.id

    def boundingRect(self):
        return QRectF(0, 0, 70, 70)

    def paint(self, painter, option, widget):
        source = QRectF(0, 0, 96, 96)
        target = QRectF(0, 0, 70, 70)
        image = QPixmap()
        if self.id == 'Red':
            image = QPixmap("player_red.png")
        elif self.id == 'Blue':
            image = QPixmap("player_blue.png")
        elif self.id == 'Yellow':
            image = QPixmap("player_yellow.png")
        elif self.id == 'Green':
            image = QPixmap("player_green.png")
        painter.drawPixmap(target, image, source)
