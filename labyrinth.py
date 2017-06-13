# Import Python modules
from collections import deque
from random import shuffle

# Import Qt modules
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QBrush

# Import custom modules
from button import Button
from arrow_button import ArrowButton
from game_board import GameBoard
from player import Player
from maze_piece import Maze
from card import Card


class Labyrinth(QGraphicsView):
    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFixedSize(1024, 768)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1024, 768)
        self.setScene(self.scene)

        # Create the GameBoard object
        self.gameboard = GameBoard(['Player1', 'Player2', 'Player3', 'Player4'])

        self.treasures = ['Bag of Gold Coins', 'Bat', 'Book', 'Dragon', 'Ghost in bottle', 'Ghost waving',
                     'Gold Crown', 'Gold Menorah', 'Gold Ring', 'Helmet', 'Jewel', 'Lady Pig', 'Lizard',
                     'Moth', 'Owl', 'Rat', 'Scarab', 'Keys', 'Skull', 'Sorceress', 'Spider',
                     'Sword', 'Treasure Chest', 'Treasure Map']

        self.player_red = Player('Red')
        self.player_blue = Player('Blue')
        self.player_yellow = Player('Yellow')
        self.player_green = Player('Green')
        self.player_list = [self.player_red, self.player_blue, self.player_yellow, self.player_green]
        self.player_queue = deque([self.player_red, self.player_blue, self.player_yellow, self.player_green])
        self.current_player = None

        self.arrow_list = None

        self.turn_tracker = QGraphicsTextItem()

        play_button = Button(QRectF(0, 0, 200, 50), "Play")
        play_button.setPos(100, 100)
        self.scene.addItem(play_button)

        play_button.sender.pressed.connect(self.start)

    def start(self):
        self.scene.clear()
        self.draw_gui()
        self.setup_board()
        self.setup_maze()
        self.deal_card()
        self.draw_cards()
        self.setup_players()
        self.change_player()

        self.lock_player(self.current_player)

    def draw_gui(self):
        # Draw a horizontal separator
        hsep = QGraphicsRectItem()
        hsep.setRect(0, 0, 10, 768)
        brush = QBrush()
        brush.setStyle(Qt.SolidPattern)
        brush.setColor(Qt.darkCyan)
        hsep.setBrush(brush)
        hsep.setPos(750, 0)
        self.scene.addItem(hsep)

        # Draw a vertical separator
        vsep = QGraphicsRectItem()
        vsep.setRect(0, 0, 264, 10)
        vsep.setBrush(brush)
        vsep.setPos(760, 250)
        self.scene.addItem(vsep)

        # Add the arrow buttons
        top1_arrow = ArrowButton()
        top1_arrow.setPos(174, 40)
        self.scene.addItem(top1_arrow)
        top2_arrow = ArrowButton()
        top2_arrow.setPos(360, 40)
        self.scene.addItem(top2_arrow)
        top3_arrow = ArrowButton()
        top3_arrow.setPos(546, 40)
        self.scene.addItem(top3_arrow)

        bottom1_arrow = ArrowButton()
        bottom1_arrow.setRotation(180)
        bottom1_arrow.setPos(204, 725)
        self.scene.addItem(bottom1_arrow)
        bottom2_arrow = ArrowButton()
        bottom2_arrow.setRotation(180)
        bottom2_arrow.setPos(390, 725)
        self.scene.addItem(bottom2_arrow)
        bottom3_arrow = ArrowButton()
        bottom3_arrow.setRotation(180)
        bottom3_arrow.setPos(576, 725)
        self.scene.addItem(bottom3_arrow)

        left1_arrow = ArrowButton()
        left1_arrow.setRotation(-90)
        left1_arrow.setPos(30, 213)
        self.scene.addItem(left1_arrow)
        left2_arrow = ArrowButton()
        left2_arrow.setRotation(-90)
        left2_arrow.setPos(30, 395)
        self.scene.addItem(left2_arrow)
        left3_arrow = ArrowButton()
        left3_arrow.setRotation(-90)
        left3_arrow.setPos(30, 580)
        self.scene.addItem(left3_arrow)

        right1_arrow = ArrowButton()
        right1_arrow.setRotation(90)
        right1_arrow.setPos(717, 183)
        self.scene.addItem(right1_arrow)
        right2_arrow = ArrowButton()
        right2_arrow.setRotation(90)
        right2_arrow.setPos(717, 365)
        self.scene.addItem(right2_arrow)
        right3_arrow = ArrowButton()
        right3_arrow.setRotation(90)
        right3_arrow.setPos(717, 550)
        self.scene.addItem(right3_arrow)

        self.arrow_list = [top1_arrow, top2_arrow, top3_arrow,
                           bottom1_arrow, bottom2_arrow, bottom3_arrow,
                           left1_arrow, left2_arrow, left3_arrow,
                           right1_arrow, right2_arrow, right3_arrow]

        self.turn_tracker.setPos(780, 300)
        self.scene.addItem(self.turn_tracker)

        # Button for left turn
        left_button = Button(QRectF(0, 0, 100, 30), 'Turn left')
        left_button.setPos(780, 180)
        self.scene.addItem(left_button)

        # Button for right turn
        right_button = Button(QRectF(0, 0, 100, 30), 'Turn right')
        right_button.setPos(900, 180)
        self.scene.addItem(right_button)

        # Connect button signals
        left_button.sender.pressed.connect(self.turn_left)
        right_button.sender.pressed.connect(self.turn_right)

        # Connect arrow signals
        top1_arrow.sender.pressed.connect(lambda: self.move_down(1))
        top2_arrow.sender.pressed.connect(lambda: self.move_down(3))
        top3_arrow.sender.pressed.connect(lambda: self.move_down(5))
        bottom1_arrow.sender.pressed.connect(lambda: self.move_up(1))
        bottom2_arrow.sender.pressed.connect(lambda: self.move_up(3))
        bottom3_arrow.sender.pressed.connect(lambda: self.move_up(5))
        left1_arrow.sender.pressed.connect(lambda: self.move_left(1))
        left2_arrow.sender.pressed.connect(lambda: self.move_left(3))
        left3_arrow.sender.pressed.connect(lambda: self.move_left(5))
        right1_arrow.sender.pressed.connect(lambda: self.move_right(1))
        right2_arrow.sender.pressed.connect(lambda: self.move_right(3))
        right3_arrow.sender.pressed.connect(lambda: self.move_right(5))

    def setup_board(self):
        # Add the GameBoard object to the scene
        for i, maze_pieces in enumerate(self.gameboard.maze_pieces):
            for j, maze in enumerate(maze_pieces):
                pos = self.gameboard.coordinates[i][j]
                # Add offset for better look
                x = pos.x() + 50
                y = pos.y() + 58
                maze.setPos(x, y)
                maze.setZValue(-1)
                self.scene.addItem(maze)

    def update_board(self):
        # Update the maze piece position
        for i, maze_pieces in enumerate(self.gameboard.maze_pieces):
            for j, maze in enumerate(maze_pieces):
                pos = self.gameboard.coordinates[i][j]
                # Add offset for better look
                x = pos.x() + 50
                y = pos.y() + 58
                maze.setPos(x, y)
                maze.update()
        # Call the neighbour calculation
        self.gameboard.create_path()
        # Update the extra maze
        self.update_maze()
        # Lock arrows
        self.lock_arrows()
        # Unlock player
        self.unlock_player(self.current_player)

    def setup_maze(self):
        """ Function for the extra maze """
        self.gameboard.current_maze.setPos(845, 50)
        self.scene.addItem(self.gameboard.current_maze)

    def update_maze(self):
        """ Function for the extra maze update """
        self.gameboard.current_maze.setPos(845, 50)

    def get_maze_coordinate(self, pos):
        x = pos.x()
        y = pos.y()
        for i, row in enumerate(self.gameboard.coordinates):
            for j, item in enumerate(row):
                if item.x() <= x <= item.x() + 93 and item.y() <= y <= item.y() + 93:
                    return (i, j)
        return (None, None)

    def setup_players(self):
        self.player_blue.setPos(77, 63)
        self.player_blue.current_coordinate = (0, 0)
        self.scene.addItem(self.player_blue)

        self.player_green.setPos(636, 63)
        self.player_green.current_coordinate = (0, 6)
        self.scene.addItem(self.player_green)

        self.player_red.setPos(77, 620)
        self.player_red.current_coordinate = (6, 0)
        self.scene.addItem(self.player_red)

        self.player_yellow.setPos(636, 620)
        self.player_yellow.current_coordinate = (6, 6)
        self.scene.addItem(self.player_yellow)

    def get_card(self):
        # Create a generator from the treasure list
        for treasure in self.treasures:
            yield treasure

    def deal_card(self):
        # Shuffle the deck
        shuffle(self.treasures)
        # Get the generator object
        gen = self.get_card()
        # Create the Card objects for the players from the generator object
        for i in range(4):
            self.player_red.cards.append(Card(next(gen)))
            self.player_blue.cards.append(Card(next(gen)))
            self.player_yellow.cards.append(Card(next(gen)))
            self.player_green.cards.append(Card(next(gen)))

    def draw_cards(self):
        self.player_red.cards[0].setPos(800, 350)
        self.scene.addItem(self.player_red.cards[0])
        self.player_red.cards[1].visible = False
        self.player_red.cards[1].setPos(900, 350)
        self.scene.addItem(self.player_red.cards[1])

        self.player_blue.cards[0].setPos(800, 480)
        self.scene.addItem(self.player_blue.cards[0])
        self.player_blue.cards[1].visible = False
        self.player_blue.cards[1].setPos(900, 480)
        self.scene.addItem(self.player_blue.cards[1])

    def change_card(self, player):
        # if the card list is not empty
        if player.cards:
            # Pop the first from the list
            player.cards.pop(0)
            print(player.id, len(player.cards))
        else:
            # If empty, we have the winner
            print('The winner is:', player.id)
            print(player.id, len(player.cards))

    def move_player(self, player, pos=None, coordinate=None):
        # Move the player to the new scene position
        player.setPos(pos.x()+80, pos.y()+62)
        # Save the player new coordinate
        player.current_coordinate = coordinate
        # Redraw/update the player
        player.update()

    def stick_player(self, direction, num):
        if direction == 'DOWN':
            for player in self.player_list:
                c = player.current_coordinate
                row = c[0]
                col = c[1]
                if col == num:
                    if row == 6:
                        new = (0, col)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)
                    else:
                        new = (row + 1, col)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)
        elif direction == 'UP':
            for player in self.player_list:
                c = player.current_coordinate
                row = c[0]
                col = c[1]
                if col == num:
                    if row == 0:
                        new = (6, col)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)
                    else:
                        new = (row - 1, col)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)
        elif direction == 'LEFT':
            for player in self.player_list:
                c = player.current_coordinate
                row = c[0]
                col = c[1]
                if row == num:
                    if col == 6:
                        new = (row, 0)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)
                    else:
                        new = (row, col + 1)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)
        elif direction == 'RIGHT':
            for player in self.player_list:
                c = player.current_coordinate
                row = c[0]
                col = c[1]
                if row == num:
                    if col == 0:
                        new = (row, 6)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)
                    else:
                        new = (row, col - 1)
                        # Get maze position on the scene from the coordinates
                        pos = self.gameboard.coordinates[new[0]][new[1]]
                        self.move_player(player, pos, new)

    def lock_player(self, player):
        player.locked = True

    def unlock_player(self, player):
        player.locked = False

    def change_player(self, player=None):
        if player is not None:
            self.player_queue.append(player)
        self.current_player = self.player_queue.popleft()
        self.turn_tracker.setPlainText('Next player: ' + self.current_player.id)

    def check_treasure(self, treasure, maze):
        if treasure == maze.treasure:
            return True
        else:
            return False

    def lock_arrows(self):
        for arrow in self.arrow_list:
            arrow.locked = True

    def unlock_arrows(self):
        for arrow in self.arrow_list:
            arrow.locked = False

    def turn_left(self):
        """ Slot for left_button """
        # Call the GameBoard object turn_left function
        self.gameboard.current_maze.turn_left()

    def turn_right(self):
        """ Slot for right_button """
        # Call the GameBoard object turn_left function
        self.gameboard.current_maze.turn_left()

    def move_up(self, pos):
        # Move the column up
        self.gameboard.move_col_up(pos)
        self.stick_player('UP', pos)
        self.update_board()

    def move_down(self, pos):
        # Move the column down
        self.gameboard.move_col_down(pos)
        self.stick_player('DOWN', pos)
        self.update_board()

    def move_left(self, pos):
        # Move the row left
        self.gameboard.move_row_left(pos)
        self.stick_player('LEFT', pos)
        self.update_board()

    def move_right(self, pos):
        # Move the row right
        self.gameboard.move_row_right(pos)
        self.stick_player('RIGHT', pos)
        self.update_board()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Return the items under the given position
            for item in self.items(event.pos()):
                # Handle the mouse click
                if isinstance(item, Maze) and not self.current_player.locked:
                    # Get the player current coordinate
                    current = self.current_player.current_coordinate
                    # Get maze coordinate
                    new = self.get_maze_coordinate(item.pos())
                    print('\tcurrent:', current, 'new:', new)
                    # Get maze position on the scene from the coordinates
                    pos = self.gameboard.coordinates[new[0]][new[1]]
                    # Validate the player path
                    valid = self.gameboard.valid_path(current, new)
                    print('\tvalid:', valid)
                    if valid:
                        # Move the player to the selected maze position
                        self.move_player(self.current_player, pos, new)
                        # Check the treasure
                        if self.check_treasure(self.current_player.cards[0].treasure, item):
                            print('Player:', self.current_player.id, 'found:', item.treasure)
                            # If found, get the next
                            self.change_card(self.current_player)
                        # Lock the player
                        self.lock_player(self.current_player)
                        # Unlock the arrows
                        self.unlock_arrows()
                        # Change player
                        self.change_player(self.current_player)
                    else:
                        print('\tInvalid move')

        else:
            # Call the original mouse event to capture other events
            (QGraphicsView, self).mouseReleaseEvent(event)


