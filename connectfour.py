import math, random, time
from profilehooks import profile

# so notes on keeping track of important things

# runs can be updated whenever a peg is placed
# threats need to be updated in a 6 by 6 box around every placed peg, this is slow as dirt


# self.board[row][column]

class Root_Node:
    def __init__(self):
        self.board = [[0 for x in range(0, 7)] for x in range(0, 6)]
        self.runs = {}
        # how many squares to add to a location to move a certain direction on the grid
        self.dmap = {0:(1, -1), 1:(0, -1), 2:(-1, -1), 3:(-1, 0), 4:(-1, 1), 5:(0, 1), 6:(1, 1), 7:(1, 0)}
        self.opposite = {0:4, 1:5, 2:6, 3:7, 4:0, 5:1, 6:2, 7:3}
            #       2 3 4
            #       1 A 5
            #       0 7 6
        for row in range(0, 6):
            for column in range(0, 7):
                self.runs[(row, column)] = [0, 0, 0, 0, 0, 0, 0, 0]
        
        self.threats = set() # set of int threats, sign determines side

        self.side_to_move = 1

    def update(self, position): # takes a positon from the engine and updates our internal position
        for i in range(0, len(self.board[0]) * len(self.board)):
            if self.board[i / 7][i % 7] == 0 and position[i] == 1: # TODO make sure this works
                self.board[i / 7][i % 7] = -1
    def update_direction(self, square, direction): # todo dont go down
        path = self.traverse(square, direction) 
        while True:
            current_loc = path.next()
            if self.is_valid(current_loc):
                current_board_value = self.tuple_to_board_value(current_loc)
                if current_board_value == 0 or current_board_value == self.board[square[0]][square[1]]:
                    # the following line might need to be just =
                    self.runs[current_loc][self.opposite[direction]] += self.tuple_to_board_value(square)
                    self.runs[current_loc][self.opposite[direction]] += self.runs[(current_loc[0] + self.dmap[self.opposite[direction]][0], current_loc[1] + self.dmap[self.opposite[direction]][1])][self.opposite[direction]]
                    # need to grab from both directions
                    
                    if current_board_value == 0 :
                        self.update_threats(current_loc, direction)
                        break # we break when we hit an enemy or blank block 
                else:
                    break
                    # we are at an enemy square, break
            else:
                # we went out of bounds of the board
                break
    # HELPER FUNCTIONS FOR BOARD INTERACTION
    def tuple_to_board_value(self, t):
        return self.board[t[0]][t[1]]
    def number_to_board_value(self, n): # given a number (0-41) returns the value of that board location
        return self.board[n / 7][n % 7]
    def board_tuple_to_number(self, t): # given a tuple for a cordinate of the board, return the numeric value
        return t[0] * 7 + t[1]
    def traverse(self, location, direction): # generator of all the squares in the direction you give, location as a tuple, direction as an int
        current_loc = location
        while True:
            current_loc = self.traverse_step(current_loc, direction)
            yield current_loc
    def traverse_step(self, location, direction):
        return (location[0] + self.dmap[direction][0], location[1] + self.dmap[direction][1])
    def is_valid(self, location):
        return location[0] in range(0, 6) and location[1] in range(0, 7) # this can be made dramatically more efficent
    def update_threats(self, location, direction): # Takes only one direction, automatically checks both direction
        if abs(self.runs[location][direction]) == 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][direction])]))
        elif abs(self.runs[location][self.opposite[direction]]) == 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][self.opposite[direction]])]))
        elif abs(self.runs[location][direction] + self.runs[location][self.opposite[direction]]) >= 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][direction])]))
    def valid_directions(self, a):
        return [x for x in self.dmap.keys() if self.is_valid(self.traverse_step(a, x))]
    
    def remove_old_threats(self):
        for threat in self.threats:
            if number_to_board_value(abs(threat)) != 0:
                self.threats.remove(threat)
                
    def display_board(self):
        for row in self.board:
            print row
    def make_move(self, column):
        for row in range(0, len(self.board)):
            if self.board[(len(self.board) - 1) - row][column] == 0:
                self.board[(len(self.board) - 1) - row][column] = self.side_to_move
                for direction in self.valid_directions(((len(self.board) - 1) - row, column)):
                    self.update_direction(( (len(self.board) - 1) - row, column), direction)
                self.side_to_move *= -1
                break
    def legal_moves(self):
        return [x for x in range(0, 7) if self.board[0][x] == 0]


class Game:
    def __init__(self):
        self.settings = []
    def set_setting(self, setting, value):
        self.settings[setting] = value
for x in range(0, 3):
    foo = Root_Node()
    start = time.time()
    counter = 0
    while time.time() - start < 5:
        counter += 1
        if len(foo.legal_moves()) == 0:
            foo = Root_Node()
        else:
            foo.make_move(random.choice(foo.legal_moves()))
    print counter
"""
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
"""
