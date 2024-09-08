import random
from random import choice

class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    def reset(self):
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()
        self.spawn()

    def spawn(self):
        new_element = 4 if random.randrange(100) > 89 else 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def move(self, direction):
        def move_row_left(row):
            # Function to collapse the row by removing zeros and merging tiles
            def tighten(row):
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            # Function to merge the row and update the score
            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]  # Update the score
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)  
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row

            return tighten(merge(tighten(row)))

        moves = {
            'Left': lambda field: [move_row_left(row) for row in field],
            'Right': lambda field: self.invert(moves['Left'](self.invert(field))),
            'Up': lambda field: self.transpose(moves['Left'](self.transpose(field))),
            'Down': lambda field: self.transpose(moves['Right'](self.transpose(field))),
        }

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()  # Spawn a new tile after a successful move
                return True
            else:
                return False

    def transpose(self, field):
        return [list(row) for row in zip(*field)]

    def invert(self, field):
        return [row[::-1] for row in field]

    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in ['Left', 'Right', 'Up', 'Down'])

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i] == row[i + 1]:
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

        check = {
            'Left': lambda field: any(row_is_left_movable(row) for row in field),
            'Right': lambda field: check['Left'](self.invert(field)),
            'Up': lambda field: check['Left'](self.transpose(field)),
            'Down': lambda field: check['Right'](self.transpose(field)),
        }

        if direction in check:
            return check[direction](self.field)
        else:
            return False