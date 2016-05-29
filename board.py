import math, copy
from sys import stderr, stdin, stdout

class Root_Node:
    def __init__(self, setup=True):
        self.board = []
        self.runs = {}
        if setup:
            for row in range(0, 6):
                for column in range(0, 7):
                    self.runs[(row, column)] = [0, 0, 0, 0, 0, 0, 0, 0]
            self.board = [[0 for x in range(0, 7)] for x in range(0, 6)]

        
            
        # how many squares to add to a location to move a certain direction on the grid
        self.dmap = {0:(1, -1), 1:(0, -1), 2:(-1, -1), 3:(-1, 0), 4:(-1, 1), 5:(0, 1), 6:(1, 1), 7:(1, 0)}
        # the opposite of each direction, might be better to do + 4 % 7 or something
        self.opposite = {0:4, 1:5, 2:6, 3:7, 4:0, 5:1, 6:2, 7:3}
            #       2 3 4
            #       1 A 5
            #       0 7 6

        # becomes true when there is a four in a row on the board
        self.won = False

        self.next = [0 for x in range(0, 7)]

        self.threats = set() # set of int threats, sign determines side
        self.side_to_move = 1
    def gethash(self):
        return str(self.board)
    
    def update(self, position): # takes a positon from the engine and updates our internal position
        for i in range(0, 42):
            if self.board[i / 7][i % 7] == 0 and position[i] in ['1', '2']:
                self.make_move(i % 7) # TODO theres a faster way to do this, but the difference is small
    def update_direction(self, square, direction): 
        path = self.traverse(square, direction)
        current_loc = next(path)
        base_board_value = self.board[square[0]][square[1]]
        starting_value = 1
        if math.copysign(1, self.runs[square][self.opposite[direction]]) == base_board_value:
            starting_value = abs(self.runs[square][self.opposite[direction]]) + 1
        while self.is_valid(current_loc):
            current_board_value = self.board[current_loc[0]][current_loc[1]]
            if current_board_value == 0:
                self.runs[current_loc][self.opposite[direction]] = starting_value * base_board_value
                self.update_threats(current_loc, direction)
                break # we break when we hit an enemy or blank block
            elif current_board_value == base_board_value:
                starting_value += 1
            else:
                break
                # we are at an enemy square, break
            current_loc = next(path)

    # HELPER FUNCTIONS FOR BOARD INTERACTION
	# if we are going to have these functions they should be memoized
    def board_tuple_to_number(self, t): # given a tuple for a cordinate of the board, return the numeric value
        return t[0] * 7 + t[1]
    def traverse(self, location, direction): # generator of all the squares in the direction you give, location as a tuple, direction as an int
        current_loc = location
        while True:
            current_loc = (current_loc[0] + self.dmap[direction][0], current_loc[1] + self.dmap[direction][1])
            yield current_loc
    def traverse_step(self, location, direction):
        return (location[0] + self.dmap[direction][0], location[1] + self.dmap[direction][1])
    def is_valid(self, location):
        return location[0] >= 0 and location[0] < 6 and location[1] >= 0 and location[1] < 7
    # optimized 1/2/16 abs does not slow it down significantly
    def update_threats(self, location, direction): # Takes only one direction, automatically checks both direction
        # this might not work properly because of the elifs, should it always check both directions?
        first_direction = self.runs[location][direction]
        opposite_direction = self.runs[location][self.opposite[direction]]
        if abs(first_direction) == 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][direction])]))
        if abs(opposite_direction) == 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][self.opposite[direction]])]))
        elif abs(first_direction + opposite_direction) >= 3: # this is checked if A or not B, optimization?
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][direction])]))
    # optimized 1/2/16, faster than a for loop or a lambda function
    # does not return up, because we never search up
    def valid_directions(self, a):
        return [x for x in list(self.dmap.keys()) if self.is_valid(self.traverse_step(a, x)) and x != 7]
               
    def display_board(self):
        for row in self.board:
            stderr.write(str([x.zfill(2) for x in list(map(str, row))]) + '\n')
            stderr.flush()
    #@profile
    def make_move(self, column):
        for row in range(0, len(self.board)):
            board_int = self.board_tuple_to_number( ((len(self.board) - 1) - row, column))
            if self.board[(len(self.board) - 1) - row][column] == 0:
                self.board[(len(self.board) - 1) - row][column] = self.side_to_move
                # remove the threat if its in our threat list
                if board_int in self.threats:
                    self.threats.remove(board_int)
                    if 1 == self.side_to_move:
                        self.won = True
                if -1 * board_int in self.threats:
                    self.threats.remove(-1 * board_int)
                    if -1 == self.side_to_move:
                        self.won = True
                for direction in self.valid_directions(((len(self.board) - 1) - row, column)):
                    self.update_direction(( (len(self.board) - 1) - row, column), direction)
                self.side_to_move *= -1
                break
        self.current_score = "nan"
    def legal_moves(self):
        return sorted([x for x in range(0, 7) if self.board[0][x] == 0], key=lambda k: abs(3 - k))
    def score(self): # todo detect hanging threats sooner, its faster
        score = 0

        # i think we can always assume that the person who won did it last move
        if self.won:
            return 10000 * -1 * self.side_to_move
        hanging_threats = []
        immeadiate_threats = []
        for threat in self.threats:
			# if the square below the threat is valid and is empty
            if abs(threat) + 7 in range(0, 42) and self.board[int((abs(threat) + 7) / 7)][int((abs(threat) + 7) % 7)] == 0:
                hanging_threats.append(threat)
            else:
                immeadiate_threats.append(threat)
        for threat in immeadiate_threats:
            if math.copysign(1, threat) == self.side_to_move:
                return 9999 * self.side_to_move
        # maybe only do hanging threats, but we have a different way to calculate this, so idk if this is needed
        score += len([x for x in self.threats if x > 0])
        score -= len([x for x in self.threats if x < 0])

        return score
    def export(self):
        child = Root_Node(False)
        child.board = [x[:] for x in self.board]
        child.runs = {k:v[:] for k,v in list(self.runs.items())}
        child.threats = copy.copy(self.threats)
        child.side_to_move = self.side_to_move
        return child
