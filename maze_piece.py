# Import Qt modules
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QColor, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsItem

TSHAPE = [[1, 1, 1],
          [0, 0, 0],
          [1, 0, 1]]

LSHAPE = [[1, 0, 1],
          [1, 0, 0],
          [1, 1, 1]]

ISHAPE = [[1, 0, 1],
          [1, 0, 1],
          [1, 0, 1]]


class Maze(QGraphicsItem):
    """
    A set of 34 Maze cards:
        - [x6] L Shape with treasure
        - [x6] T Shape with treasure
        - [x9] L Shape empty
        - [x13] I Shape empty
    """
    def __init__(self, shape, treasure=None, player=None):
        QGraphicsItem.__init__(self)
        self.shape = shape
        self.treasure = treasure
        self.player = player
        self.PENWIDTH = 3

        self.treasures = ['Bag of Gold Coins', 'Bat', 'Book', 'Dragon', 'Ghost in bottle', 'Ghost waving',
                     'Gold Crown', 'Gold Menorah', 'Gold Ring', 'Helmet', 'Jewel', 'Lady Pig', 'Lizard',
                     'Moth', 'Owl', 'Rat', 'Scarab', 'Keys', 'Skull', 'Sorceress', 'Spider',
                     'Sword', 'Treasure Chest', 'Treasure Map']

        # Setup the coordinates
        self.coordinates = []
        tx = 0; ty = 0
        bx = 30; by = 30
        for i in range(3):
            tmp = []
            for j in range(3):
                pos = QRectF(tx, ty, bx, by)
                tmp.append(pos)
                tx += 30
            # Build a list of list
            self.coordinates.append(tmp)
            ty += 30
            tx -= 90

    def boundingRect(self):
        # Always adjust the boundingRect with the pen width
        return QRectF(0 - self.PENWIDTH/2.0, 0 - self.PENWIDTH/2.0,
                      90 + self.PENWIDTH, 90 + self.PENWIDTH)

    def load_image(self, name):
        image = QPixmap()
        if name in self.treasures:
            image = QPixmap('/home/zolcsi/Documents/Labyrinth/maze/' + name + ".png")
        return image

    def paint(self, painter, option, widget):
        # Draw an outer frame
        pen = QPen()
        pen.setWidth(self.PENWIDTH)
        pen.setColor(Qt.black)
        painter.setPen(pen)
        painter.drawRect(QRectF(0, 0, 90, 90))

        # Draw the individual pieces based on the shape
        for i in range(3):
            for j in range(3):
                rect = self.coordinates[i][j]
                if self.shape[i][j] == 0:
                    painter.setBrush(QColor(Qt.white))
                    painter.setPen(QColor(Qt.white))
                else:
                    painter.setBrush(QColor(Qt.darkGreen))
                    painter.setPen(QColor(Qt.darkGreen))
                painter.drawRect(rect)

        # Draw treasure if exist
        if self.treasure is not None:
            source = QRectF(0, 0, 640, 480)
            target = QRectF(10, 10, 70, 70)
            image = self.load_image(self.treasure)
            painter.drawPixmap(target, image, source)

        # Draw player pos if exist
        if self.player is not None:
            if self.player == 'RED':
                painter.setBrush(QColor(Qt.red))
                painter.setPen(QColor(Qt.red))
            elif self.player == 'BLUE':
                painter.setBrush(QColor(Qt.blue))
                painter.setPen(QColor(Qt.blue))
            elif self.player == 'YELLOW':
                painter.setBrush(QColor(Qt.yellow))
                painter.setPen(QColor(Qt.yellow))
            elif self.player == 'GREEN':
                painter.setBrush(QColor(Qt.green))
                painter.setPen(QColor(Qt.green))
            painter.drawEllipse(self.boundingRect().center(), 20, 20)

    def turn_right(self):
        """ Rotate the shape matrix right """
        self.shape = list(zip(*self.shape[::-1]))
        self.update()

    def turn_left(self):
        """ Rotate the shape matrix left """
        self.shape = list(zip(*self.shape))[::-1]
        self.update()

    def get_path(self):
        path = []
        if self.shape[0][1] == 0:
            path.append('0')
        else:
            path.append(None)
        if self.shape[1][2] == 0:
            path.append('0')
        else:
            path.append(None)
        if self.shape[2][1] == 0:
            path.append('0')
        else:
            path.append(None)
        if self.shape[1][0] == 0:
            path.append('0')
        else:
            path.append(None)
        return path


if __name__ == "__main__":
    maze = Maze(LSHAPE, treasure='Lizard')
    print(maze.get_path())
    for i in maze.shape:
        print(i)