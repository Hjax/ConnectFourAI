import math

foo = [0 for x in range(0, 42)]
foo[5] = 1
def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

# so notes on keeping track of important things

# runs can be updated whenever a peg is placed
# threats need to be updated in a 6 by 6 box around every placed peg, this is slow as dirt

class Root_Node:
    def __init__(self):
        self.board = [0 for x in range(0, 42)]
        self.runs = {}
        for i in range(0, 42):
            #       2   3
            #       1 A 4
            #       0 6 5
        
            self.runs[i] = [0, 0, 0, 0, 0, 0, 0]

        # since im about to go to bed and dont have time to implement it,
        # give every square 5 values, since it can be the end point in 5 ways
        # scoring with total number of ally and enemy runs that end at that place might be cool
        
        self.threats_allied = []
        self.threats_enemy = []

        self.side_to_move = 1
        # runs and threes are a list of integers, positive for allies,
        # negitive for enemies
    def update(self, position): # takes a positon from the engine and updates our internal position
        for i in range(0, len(self.board)):
            if self.board[i] == 0 and position[i] == 1:
                self.board[i] = -1
    def columns(self):
        return [self.board[x:][::7] for x in range(0, 7)]
    def rows(self):
        return [self.board[i:i + 7] for i in range(0, len(self.board), 7)]
    def opposite(self, direction):
        mapper = [0:4, 1:5, 2:6, 4:0, 5:1, 6:2]
        return mapper[direction]
    def update_direction(self, square, direction):
        current_loc = square
        dmap = {0:6, 1:-1, 2:-8, 3:-6, 4:1, 5:8, 6:7}
        while True:
            current_loc += dmap[direction]
            if square in range(0, 42):
                if self.board[i] == 0:
                    self.runs[current][opposite]
                    
                    if direction == 3:
                        if self.runs[current][3] == -3:
                            pass
                        elif self.runs[current][3] == 3:
                            pass
                    else:
                        
                        if self.runs[current][direction] == -3:

                        elif self.runs[current][direction] == 3:

                        if self.runs[current][self.opposite(direction)] == 3:

                        elif self.runs[current][self.opposite(direction)] == -3:

                        if self.runs[current][direction] + self.runs[current][self.opposite(direction)] == -3:
                        
                        elif self.runs[current][direction] + self.runs[current][self.opposite(direction)] == 3:

                    break # we break when we hit an enemy or blank block 
                if self.board[i] != self.board[square]:
                    break
                else:
                    pass
                    # we are at an allied square, nothing to do except continue updating in the same direction
            else:
                # we went out of bounds of the board
                break
            
        
    def display_board(self):
        rows = self.rows()
        for row in rows:
            print row
    def make_move(self, column):
        rows = self.rows()
        for row in range(0, len(rows)):
            if rows[(len(rows) - 1) - row][column] == 0:
                self.board[(7 * ((len(rows) - 1) - row))+ column] = self.side_to_move
                break
    def legal_moves(self):
        return [x for x in range(0, 7) if self.board[x] == 0]


class Game:
    def __init__(self):
        self.settings = []
    def set_setting(self, setting, value):
        self.settings[setting] = value
    

while True:
    break
    connectfour = Game()
    root = Node()
    read_line = raw_input()
    processed = read_line.split(" ")
    if processed[0] == "settings":
        connectfour.set_setting(processed[1], processed[2])
    if processed[0] == "update":
        if processed[1] == "field":
            root.update(processed[2].replace(";", ",").split[","])
