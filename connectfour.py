import math, random, time
import copy
from minimax import Search
from sys import stderr, stdin, stdout
#from profilehooks import profile

# so notes on keeping track of important things

# runs can be updated whenever a peg is placed
# threats need to be updated in a 6 by 6 box around every placed peg, this is slow as dirt


# self.board[row][column]

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

        self.threats = set() # set of int threats, sign determines side
        self.pieces_played = 0
        self.side_to_move = 1
    def gethash(self):
        return str(self.board)
    
    def update(self, position): # takes a positon from the engine and updates our internal position
        for i in range(0, 42):
            if self.board[i / 7][i % 7] == 0 and position[i] in ['1', '2']:
                self.make_move(i % 7) # TODO theres a faster way to do this, but the difference is small
                    
    def update_direction(self, square, direction): 
        if direction == 7: # we dont need to traverse downwards 
            return
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
    def valid_directions(self, a):
        return [x for x in list(self.dmap.keys()) if self.is_valid(self.traverse_step(a, x))]
               
    def display_board(self):
        for row in self.board:
            stderr.write(str([x.zfill(2) for x in list(map(str, row))]) + '\n')
            stderr.flush()
    def make_move(self, column):
        for row in range(0, len(self.board)):
            if self.board[(len(self.board) - 1) - row][column] == 0:
                self.board[(len(self.board) - 1) - row][column] = self.side_to_move
                # remove the threat if its in our threat list
                self.pieces_played += 1
                if self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ) in self.threats:
                    self.threats.remove(self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ))
                    if math.copysign(1, self.board_tuple_to_number(((len(self.board) - 1) - row, column))) == self.side_to_move:
                        self.won = True
                if -1 * self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ) in self.threats:
                    self.threats.remove(-1 * self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ))
                    if math.copysign(1, -1 * self.board_tuple_to_number(((len(self.board) - 1) - row, column))) == self.side_to_move:
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
        child.pieces_played = self.pieces_played
        return child

if __name__ == "__main_1_" :
    connectfour = Search(Root_Node())
    while True:
        read_line = stdin.readline()
        if len(read_line) == 0:
            break
        line = read_line.strip()
        if len(line) == 0:
            continue
        processed = line.split(" ")
        if processed[0] == "settings":
            connectfour.set_setting(processed[1], processed[2])
        if processed[0] == "update":
            if processed[1] == "game":
                if processed[2] == "field":
                    connectfour.root.update(processed[3].replace(";", ",").split(","))
                if processed[2] == "round":
                    connectfour.set_setting(processed[2], processed[3])
                connectfour.set_setting(processed[1], processed[2])
        if processed[0] == "action":
            start = time.time()
            connectfour.set_setting("current_time", processed[2])
            connectfour.go()
            stderr.write("Searched %s nodes in %s seconds \n" % (str(connectfour.nodes), str(time.time() - start)))
            stderr.flush()
if __name__ == "__main__" :
    connectfour = Search(Root_Node())
    while True:

        connectfour.settings['current_time'] = 6000
        start = time.time()
        connectfour.go()
        print("searched %s nodes in %s seconds" % (str(connectfour.nodes), str(time.time() - start)))
        connectfour.root.display_board()
        connectfour.nodes = 0
        connectfour.root.make_move(int(input()))

def test_speed():
    print("")
    for x in range(0, 3):
        foo = Root_Node()
        start = time.time()
        counter = 0
        while time.time() - start < 1:
            counter += 1
            if len(foo.legal_moves()) == 0 or foo.won:
                foo = Root_Node()
            else:
                foo.export()
                foo.make_move(random.choice(foo.legal_moves()))
                foo.score()
        print(counter)
        assert counter > 1000
def test_threats_simple():
    foo = Root_Node()
    foo.make_move(0)
    foo.make_move(6)
    foo.make_move(1)
    foo.make_move(5)
    foo.make_move(2)
    assert 38 in foo.threats
    assert -38 not in foo.threats
    foo.make_move(4)
    assert -38 in foo.threats
    assert 38 in foo.threats
    foo.make_move(3)
    assert -38 not in foo.threats
    assert 38 not in foo.threats
def test_traverse():
    foo = Root_Node()
    bar = foo.traverse((1, 2), 6)
    assert next(bar) == (2, 3)
    assert next(bar) == (3, 4)
def test_square_validity():
    foo = Root_Node()
    assert not foo.is_valid((-1, 5))
    for i in range(0, 7):
        for x in range(0, 6):
            assert foo.is_valid((x, i))
def test_full_game():
    foo = Root_Node()
    for i in "4444452322223353347777362177555511111":
        foo.make_move(int(i) - 1)
    assert foo.board == [[1, 1, 1, -1, -1, 0, -1], [-1, -1, 1, 1, 1, 0, 1], [1, 1, -1, -1, -1, 0, -1], [-1, -1, -1, 1, 1, 0, 1], [1, 1, 1, -1, 1, 0, -1], [-1, 1, -1, 1, -1, -1, 1]]
    assert foo.threats == set([26.0, -5.0, 12.0, -19.0])
def test_node_export():
    foo = Root_Node()
    foo.make_move(0)
    bar = foo.export()
    foo.make_move(0)
    foo.make_move(1)
    foo.make_move(1)
    foo.make_move(2)
    foo.make_move(2)
    assert bar.board != foo.board
    assert bar.runs != foo.runs
    assert bar.threats != foo.threats
    assert bar.side_to_move != foo.side_to_move
