"""

The game board (with 16 maze pieces affixed, with space for 34 more pieces.)

Creature Right-Angle Corridor Maze piece [x6], one each of the following:
    - Lizard
    - Moth
    - Owl
    - Scarab
    - Rat
    - Spider with Web

Creature Straight Corridor Maze piece [x6], one each of the following:
    - Bat
    - Dragon
    - Ghost in Bottle
    - Ghost (waving)
    - Lady Pig
    - Sorceress

Empty Right-Angle Corridor Maze piece. [x9]
Empty Straight Corridor Maze piece. [x13]

"""

# Import Qt modules
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsRectItem

# Import python modules
from random import shuffle
from collections import deque

# Import custom modules
from maze_piece import Maze, TSHAPE, LSHAPE, ISHAPE
from graph import Graph


class GameBoard(QGraphicsRectItem):
    """
    The game board (with 16 maze pieces affixed, with space for 34 more pieces.)
    """
    def __init__(self, players=[]):
        QGraphicsRectItem.__init__(self)
        self.players = players
        self.maze_pieces = []
        self.movable_maze_pieces = []
        self.current_maze = ''
        self.graph = Graph()

        # Setup the coordinates
        self.coordinates = []
        x = 0; y = 0
        for i in range(7):
            tmp = []
            for j in range(7):
                pos = QPoint(x, y)
                tmp.append(pos)
                x += 93
            self.coordinates.append(tmp)
            y += 93
            x -= 651

        # Construct the maze pieces
        self.fix_maze()
        self.movable_maze()
        self.shuffle_maze()
        self.create_path()

    def fix_maze(self):
        """ Construct the fix maze pieces """
        maze00 = Maze(LSHAPE, player='BLUE')
        maze00.turn_right()
        maze02 = Maze(TSHAPE, treasure='Helmet')
        maze04 = Maze(TSHAPE, treasure='Gold Menorah')
        maze06 = Maze(LSHAPE, player='GREEN')
        maze06.turn_right()
        maze06.turn_right()

        maze20 = Maze(TSHAPE, treasure='Sword')
        maze20.turn_left()
        maze22 = Maze(TSHAPE, treasure='Jewel')
        maze22.turn_left()
        maze24 = Maze(TSHAPE, treasure='Treasure Chest')
        maze26 = Maze(TSHAPE, treasure='Gold Ring')
        maze26.turn_right()

        maze40 = Maze(TSHAPE, treasure='Skull')
        maze40.turn_left()
        maze42 = Maze(TSHAPE, treasure='Keys')
        maze42.turn_left()
        maze42.turn_left()
        maze44 = Maze(TSHAPE, treasure='Gold Crown')
        maze44.turn_right()
        maze46 = Maze(TSHAPE, treasure='Treasure Map')
        maze46.turn_right()

        maze60 = Maze(LSHAPE, player='RED')
        maze62 = Maze(TSHAPE, treasure='Bag of Gold Coins')
        maze62.turn_left()
        maze62.turn_left()
        maze64 = Maze(TSHAPE, treasure='Book')
        maze64.turn_left()
        maze64.turn_left()
        maze66 = Maze(LSHAPE, player='YELLOW')
        maze66.turn_left()

        self.maze_pieces = [[maze00, '', maze02, '', maze04, '', maze06],
                            ['', '', '', '', '', '', ''],
                            [maze20, '', maze22, '', maze24, '', maze26],
                            ['', '', '', '', '', '', ''],
                            [maze40, '', maze42, '', maze44, '', maze46],
                            ['', '', '', '', '', '', ''],
                            [maze60, '', maze62, '', maze64, '', maze66]]

    def movable_maze(self):
        """ Construct the movable maze pieces """
        lmaze1 = Maze(LSHAPE, treasure='Lizard')
        lmaze2 = Maze(LSHAPE, treasure='Moth')
        lmaze3 = Maze(LSHAPE, treasure='Owl')
        lmaze4 = Maze(LSHAPE, treasure='Scarab')
        lmaze5 = Maze(LSHAPE, treasure='Rat')
        lmaze6 = Maze(LSHAPE, treasure='Spider')

        lmaze7 = Maze(LSHAPE)
        lmaze8 = Maze(LSHAPE)
        lmaze9 = Maze(LSHAPE)
        lmaze10 = Maze(LSHAPE)
        lmaze11 = Maze(LSHAPE)
        lmaze12 = Maze(LSHAPE)
        lmaze13 = Maze(LSHAPE)
        lmaze14 = Maze(LSHAPE)
        lmaze15 = Maze(LSHAPE)

        tmaze1 = Maze(TSHAPE, treasure='Bat')
        tmaze2 = Maze(TSHAPE, treasure='Dragon')
        tmaze3 = Maze(TSHAPE, treasure='Ghost in bottle')
        tmaze4 = Maze(TSHAPE, treasure='Ghost waving')
        tmaze5 = Maze(TSHAPE, treasure='Lady Pig')
        tmaze6 = Maze(TSHAPE, treasure='Sorceress')

        imaze1 = Maze(ISHAPE)
        imaze2 = Maze(ISHAPE)
        imaze3 = Maze(ISHAPE)
        imaze4 = Maze(ISHAPE)
        imaze5 = Maze(ISHAPE)
        imaze6 = Maze(ISHAPE)
        imaze7 = Maze(ISHAPE)
        imaze8 = Maze(ISHAPE)
        imaze9 = Maze(ISHAPE)
        imaze10 = Maze(ISHAPE)
        imaze11 = Maze(ISHAPE)
        imaze12 = Maze(ISHAPE)
        imaze13 = Maze(ISHAPE)
        # Add the pieces to the list
        self.movable_maze_pieces = [lmaze1, lmaze2, lmaze3, lmaze4, lmaze5, lmaze6,
                            lmaze7, lmaze8, lmaze9, lmaze10, lmaze11, lmaze12,
                            lmaze13, lmaze14, lmaze15,
                            tmaze1, tmaze2, tmaze3, tmaze4, tmaze5, tmaze6,
                            imaze1, imaze2, imaze3, imaze4, imaze5, imaze6,
                            imaze7, imaze8, imaze9, imaze10, imaze11, imaze12, imaze13]

        # Randomize the movable maze order in the list
        shuffle(self.movable_maze_pieces)
        # Get the first from the list as a start maze
        self.current_maze = self.movable_maze_pieces.pop(0)

    def shuffle_maze(self):
        """ Add the movable pieces to the game board pieces """
        # Create an iterator from the movable pieces
        it_maze = iter(self.movable_maze_pieces)
        # Go over the fix board and if the item was empty add the movable piece
        for row in self.maze_pieces:
            for n, item in enumerate(row):
                if item == '':
                    row[n] = next(it_maze)

    def move_row_left(self, row):
        """ Move a row left and add the free maze to the end. Movable rows [1, 3, 5] """
        # Make a deque from the given row
        d = deque(self.maze_pieces[row])
        # Pop left and save the item
        old_maze = d.pop()
        # Append the current maze to left
        d.appendleft(self.current_maze)
        # Update the original list
        self.maze_pieces[row] = d
        # Update the current maze
        self.current_maze = old_maze

    def move_row_right(self, row):
        """ Move a row left and add the free maze to the end. Movable rows [1, 3, 5] """
        # Make a deque from the given row
        d = deque(self.maze_pieces[row])
        # Pop left and save the item
        old_maze = d.popleft()
        # Append the current maze to right
        d.append(self.current_maze)
        # Update the original list
        self.maze_pieces[row] = d
        # Update the current maze
        self.current_maze = old_maze

    def move_col_down(self, col):
        """ Move a column down and add the free maze to the top. Movable cols [1, 3, 5] """
        # Make a deque from the given column
        d = deque([row[col] for row in self.maze_pieces])
        # Pop left and save the item
        old_maze = d.pop()
        # Append the current maze to left
        d.appendleft(self.current_maze)
        # Update the original list
        for row in self.maze_pieces:
            row[col] = d.popleft()
        # Update the current maze
        self.current_maze = old_maze

    def move_col_up(self, col):
        """ Move a column up and add the free maze to the down. Movable cols [1, 3, 5] """
        # Make a deque from the given column
        d = deque([row[col] for row in self.maze_pieces])
        # Pop left and save the item
        old_maze = d.popleft()
        # Append the current maze to left
        d.append(self.current_maze)
        # Update the original list
        for row in self.maze_pieces:
            row[col] = d.popleft()
        # Update the current maze
        self.current_maze = old_maze

    def neighbour(self, x, y, w=7, h=7):
        """
        Find non-diagonal neighbours in a matrix[w,h] in clockwise direction.
        Return None if neighbour is not found.
        """
        tmp = []
        for a in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            if (0 <= x + a[0] < w) and (0 <= y + a[1] < h):
                tmp.append((x + a[0], y + a[1]))
            else:
                tmp.append((None, None))
        return tmp

    def create_path(self):
        """
        Create path (graph) from the non-diagonal neighbours
        """
        # Clear everything from the dictionary
        self.graph.vertex_list.clear()
        # Valid neighbour side check based on the rounds (k)
        side_list = [(0, 2), (1, 3), (2, 0), (3, 1)]
        # Find all non-diagonal neighbours in a 7x7 matrix
        for i in range(7):
            for j in range(7):
                # Get the neighbours
                neighbour = self.neighbour(i, j)
                # Get the current index path
                p1 = self.maze_pieces[i][j].get_path()
                # Iterate over the neighbours (nei) and keep track the rounds (k)
                for k, nei in enumerate(neighbour):
                    # If the neighbour is not empty
                    if nei != (None, None):
                        # Create a new vertex
                        self.graph.add_vertex((i, j))
                        # Get the neighbour path
                        p2 = self.maze_pieces[nei[0]][nei[1]].get_path()
                        # Save the valid side based on the rounds (k) to (v)
                        v = side_list[k]
                        # Check if the side has path (0)
                        if p1[v[0]] == '0' and p2[v[1]] == '0':
                            self.graph.add_edge((i, j), (nei[0], nei[1]))
                        p2.clear()

    def valid_path(self, start, end):
        """
        Find valid path among the non-diagonal neighbours using graph
        """
        path = self.graph.find_path(start, end)
        if path:
            return True
        else:
            return False


if __name__ == "__main__":
    # Create the GameBoard object
    gameboard = GameBoard(['Player_red', 'Player_yellow', 'Player_blue', 'Player_green'])

    def test_player_treasure():
        # Test players
        players = ['Player_red', 'Player_yellow', 'Player_blue', 'Player_green']
        for player in players:
            print('Player:', player, 'at position:', gameboard.find_player(player))

        # Test treasures
        treasures = ['Bag of Gold Coins','Bat','Book','Dragon','Ghost in bottle','Ghost waving',
                     'Gold Crown','Gold Menorah','Gold Ring','Helmet','Jewel','Lady Pig','Lizard',
                     'Moth','Owl','Rat','Scarab','Set of Keys','Skull','Sorceress','Spider',
                     'Sword','Treasure Chest','Treasure Map']
        for treasure in treasures:
            print('Treasure:', treasure, 'at position:', gameboard.find_treasure(treasure))
        print('Current maze treasure:', gameboard.current_maze.treasure)

    test_player_treasure()






