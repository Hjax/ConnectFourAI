import math, random, time
import copy
from sys import stderr, stdin, stdout

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

        self.current_score = "nan"
        # todo if a winning pieces gets put in a threat, mark the board as a win
        self.threats = set() # set of int threats, sign determines side
        self.pieces_played = 0
        self.side_to_move = 1

    def update(self, position): # takes a positon from the engine and updates our internal position
        for i in range(0, 42):
            if self.board[i / 7][i % 7] == 0 and position[i] in ['1', '2']: # TODO make sure this works
                self.make_move(i % 7) # TODO theres a faster way to do this
                    
    # note it isnt detecting enemy runs correctly
    def update_direction(self, square, direction): # todo dont go down
        path = self.traverse(square, direction)
        current_loc = path.next()
        base_board_value = self.board[square[0]][square[1]]
        if self.is_valid(current_loc):
            starting_value = abs(self.runs[square][self.opposite[direction]])
        if math.copysign(1, self.runs[square][self.opposite[direction]]) != base_board_value:
            starting_value = 0
        while self.is_valid(current_loc):
            current_board_value = self.board[current_loc[0]][current_loc[1]]
            starting_value += 1
            if current_board_value == 0:
                # the following line might need to be just =
                self.runs[current_loc][self.opposite[direction]] = starting_value * base_board_value
                self.update_threats(current_loc, direction)
                break # we break when we hit an enemy or blank block
            elif current_board_value == base_board_value:
                pass
            else:
                break
                # we are at an enemy square, break
            current_loc = path.next()

    # HELPER FUNCTIONS FOR BOARD INTERACTION
    def number_to_board_value(self, n): # given a number (0-41) returns the value of that board location
        return self.board[int(n / 7)][int(n % 7)]
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
        return location[0] >= 0 and location[0] < 6 and location[1] >= 0 and location[1] < 7
    def update_threats(self, location, direction): # Takes only one direction, automatically checks both direction
        # this might not work properly because of the elifs, should it always check both directions?
        first_direction = self.runs[location][direction]
        opposite_direction = self.runs[location][self.opposite[direction]]
        if abs(first_direction) == 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][direction])]))
        if abs(opposite_direction) == 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][self.opposite[direction]])]))
        elif abs(first_direction + opposite_direction) >= 3:
            self.threats = self.threats.union(set([self.board_tuple_to_number(location) * math.copysign(1, self.runs[location][direction])]))
    def valid_directions(self, a):
        return [x for x in self.dmap.keys() if self.is_valid(self.traverse_step(a, x))]
               
    def display_board(self):
        for row in self.board:
            print map(lambda x: x.zfill(2), map(str, row))
    def make_move(self, column):
        for row in range(0, len(self.board)):
            if self.board[(len(self.board) - 1) - row][column] == 0:
                self.board[(len(self.board) - 1) - row][column] = self.side_to_move
                # remove the threat if its in our threat list
                self.pieces_played += 1
                if self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ) in self.threats:
                    self.threats.remove(self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ))
                if -1 * self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ) in self.threats:
                    self.threats.remove(-1 * self.board_tuple_to_number( ((len(self.board) - 1) - row, column) ))
                for direction in self.valid_directions(((len(self.board) - 1) - row, column)):
                    
                    self.update_direction(( (len(self.board) - 1) - row, column), direction)
                self.side_to_move *= -1
                break
    def legal_moves(self):
        return [x for x in range(0, 7) if self.board[0][x] == 0]
    def score(self): # todo detect hanging threats sooner, its faster
        if self.current_score != "nan":
            #return self.current_score
            pass
        score = 0
        # we only return winning score for wins we can see, not forced wins though tempo, since we might lose a tempo
        winning_score = 9999999

        hanging_threats = []
        immeadiate_threats = []
        for threat in self.threats:
            if abs(threat) + 7 in range(0, 42) and self.number_to_board_value(abs(threat) + 7) == 0:
                hanging_threats.append(threat)
            else:
                immeadiate_threats.append(threat)
        self.immeadiate_threats = immeadiate_threats
        for threat in immeadiate_threats:
            if math.copysign(1, threat) == self.side_to_move:
                return winning_score * self.side_to_move
        # maybe only do hanging threats, but we have a different way to calculate this, so idk if this is needed
        score += len(filter(lambda x: x > 0, self.threats))
        score -= len(filter(lambda x: x < 0, self.threats))

        taken = []
        for threat in hanging_threats:
            if abs(threat) not in taken:
                taken.append(abs(threat))
            if (abs(threat) + 7) not in taken:
                taken.append(abs(threat) + 7)
            clearer = self.traverse((int(threat / 7), int(threat % 7)), 3)
            next_step = clearer.next()
            while self.is_valid(next_step):
                if self.board_tuple_to_number(next_step) not in taken:
                    taken.append(self.board_tuple_to_number(next_step))
                    next_step = clearer.next()
                else:
                    break
        # you want it to be odd when its your turn to move, even otherwise
        if self.side_to_move == 1:
            if len(filter(lambda x: x > 0, hanging_threats)) > 0 and (self.pieces_played - len(taken)) % 2 == 1:
                score += 500
            elif len(filter(lambda x: x < 0, hanging_threats)) > 0 and (self.pieces_played - len(taken)) % 2 == 0:
                score -= 500
        else:
            if len(filter(lambda x: x > 0, hanging_threats)) > 0 and (self.pieces_played - len(taken)) % 2 == 0:
                score += 500
            elif len(filter(lambda x: x < 0, hanging_threats)) > 0 and (self.pieces_played - len(taken)) % 2 == 1:
                score -= 500
        self.current_score = score
        return score
    def export(self):
        child = Root_Node()
        child.board = []
        for x in self.board:
            child.board.append(x[:])
        child.runs = {}
        for i in self.runs.keys():
            child.runs[i] = self.runs[i][:]
        child.threats = copy.copy(self.threats)
        child.side_to_move = self.side_to_move
        child.pieces_played = self.pieces_played
        return child

class Game:
    def __init__(self):
        self.settings = {}
        self.nodes = 0
        self.root = Root_Node()
    def set_setting(self, setting, value):
        self.settings[setting] = value
    def current_move_time(self): # returns the amount of time we are going to think for this move
        max_time = int(self.settings["timebank"])
        current_time = int(self.settings["current_time"])
        increment = int(self.settings["time_per_move"])
        current_round = int(self.settings["round"])
        thinking_time = (current_time + increment * (42 - current_round)) / (43 - current_round)
        return min(max(thinking_time, increment), current_time)
    def negamax(self, node, depth):
        self.nodes += 1
        if depth == 0 or abs(node.score()) > 99999:
            return node.score()
        if node.side_to_move == 1:
            bestValue = -99999999
        else:
            bestValue = 99999999
        for child in node.legal_moves():
            current_child = node.export()
            current_child.make_move(child)
            if node.side_to_move == 1:
                bestValue = max(bestValue, self.negamax(current_child, depth -1))
            else:
                bestValue = min(bestValue, self.negamax(current_child, depth -1))
        
        return bestValue
        
        
    def go(self):
        #time = self.current_move_time()
        # if we can win, we must win, this might also block enemy threats
        self.root.score()
        if len(self.root.immeadiate_threats) > 0:
            if self.root.side_to_move == -1:
                self.root.immeadiate_threats.sort()
            else:
                self.root.immeadiate_threats.sort()
                self.root.immeadiate_threats.reverse()
            #self.root.display_board()
            self.root.make_move(int(abs(self.root.immeadiate_threats[0]) % 7))
            stdout.write("place_disc %s" % (int(abs(self.root.immeadiate_threats[0]) % 7)) + '\n')
            stdout.flush()
            return
        elif int(self.settings["current_time"]) < 800:
            depth = 2
        elif int(self.settings["current_time"]) < 2000:
            depth = 3
        else:
            depth = 4
        scores = {}
        for child in self.root.legal_moves():
            current_child = self.root.export()
            current_child.make_move(child)
            scores[child] = self.negamax(current_child, depth)
        print scores
        if self.root.side_to_move == -1:
            self.root.make_move((min(scores, key=lambda k: scores[k])))
            stdout.write("place_disc %s" % (min(scores, key=lambda k: scores[k])) + '\n')
        else:
            self.root.make_move((max(scores, key=lambda k: scores[k])))
            stdout.write("place_disc %s" % (max(scores, key=lambda k: scores[k])) + '\n')
        stdout.flush()
        #self.root.display_board()

if __name__ == "__main__" :
    connectfour = Game()
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
            connectfour.set_setting("current_time", processed[2])
            connectfour.go()
if __name__ == "__main1__" :
    connectfour = Game()
    while True:
        connectfour.settings['current_time'] = 6000
        start = time.time()
        connectfour.go()
        print "searched %s nodes in %s seconds" % (str(connectfour.nodes), str(time.time() - start))
        connectfour.nodes = 0
        connectfour.root.make_move(int(raw_input()))
        connectfour.root.display_board()
def test_speed():
    print ""
    for x in range(0, 3):
        foo = Root_Node()
        start = time.time()
        counter = 0
        while time.time() - start < 1:
            counter += 1
            if len(foo.legal_moves()) == 0:
                foo = Root_Node()
            else:
                foo.make_move(random.choice(foo.legal_moves()))
                foo.score()
        print counter
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
    assert bar.next() == (2, 3)
    assert bar.next() == (3, 4)
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
    assert bar.pieces_played != foo.pieces_played
    assert bar.side_to_move != foo.side_to_move
