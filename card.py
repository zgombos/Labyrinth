"""
Fixed:
treasure='Helmet'
treasure='Gold Menorah'
treasure='Sword'
treasure='Jewel'
treasure='Treasure Chest'
treasure='Gold Ring'
treasure='Skull'
treasure='Keys'
treasure='Gold Crown'
treasure='Treasure Map'
treasure='Bag of Gold Coins'
treasure='Book'

Movable:
treasure='Lizard'
treasure='Moth'
treasure='Owl'
treasure='Scarab'
treasure='Rat'
treasure='Spider'
treasure='Bat'
treasure='Dragon'
treasure='Ghost in bottle'
treasure='Ghost waving'
treasure='Lady Pig'
treasure='Sorceress'

"""

# Import Qt modules
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import QPixmap, QPen, QColor
from PyQt5.QtCore import QRectF, Qt


class Card(QGraphicsItem):
    def __init__(self, treasure):
        QGraphicsItem.__init__(self)
        self.treasure = treasure
        self.PENWIDTH = 3
        self.visible = True
        self.treasures = ['Bag of Gold Coins', 'Bat', 'Book', 'Dragon', 'Ghost in bottle', 'Ghost waving',
                     'Gold Crown', 'Gold Menorah', 'Gold Ring', 'Helmet', 'Jewel', 'Lady Pig', 'Lizard',
                     'Moth', 'Owl', 'Rat', 'Scarab', 'Keys', 'Skull', 'Sorceress', 'Spider',
                     'Sword', 'Treasure Chest', 'Treasure Map']

    def boundingRect(self):
        # Always adjust the boundingRect with the pen width
        return QRectF(0 - self.PENWIDTH/2.0, 0 - self.PENWIDTH/2.0,
                      70 + self.PENWIDTH, 100 + self.PENWIDTH)

    def load_image(self, name):
        image = QPixmap()
        if name in self.treasures:
            image = QPixmap('/home/zolcsi/Documents/Labyrinth/maze/' + name + ".png")
        return image

    def paint(self, painter, option, widget):
        # Draw the rect
        pen = QPen()
        pen.setWidth(self.PENWIDTH)
        pen.setColor(Qt.black)
        painter.setPen(pen)
        painter.setBrush(QColor(Qt.gray))
        painter.drawRect(self.boundingRect())
        if self.visible:
            source = QRectF(0, 0, 640, 480)
            target = QRectF(0, 10, 70, 70)
            image = self.load_image(self.treasure)
            painter.drawPixmap(target, image, source)
        else:
            image = QPixmap('/home/zolcsi/Documents/Labyrinth2/card_back_236x349.jpg')
            source = QRectF(0, 0, 236, 349)
            target = QRectF(self.boundingRect())
            painter.drawPixmap(target, image, source)

