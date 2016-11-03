from __future__ import print_function

import math, random, time
import copy
from minimax import Search
from sys import stderr, stdin, stdout
from book import book

win_conds = [15, 30, 60, 120, 1920, 3840, 7680, 15360, 245760, 491520, 983040, 1966080, 31457280, 62914560, 125829120, 251658240, 4026531840, 8053063680, 16106127360, 32212254720, 515396075520, 1030792151040, 2061584302080, 4123168604160, 2113665, 4227330, 8454660, 16909320, 33818640, 67637280, 135274560, 270549120, 541098240, 1082196480, 2164392960, 4328785920, 8657571840, 17315143680, 34630287360, 69260574720, 138521149440, 277042298880, 554084597760, 1108169195520, 2216338391040, 16843009, 2130440, 33686018, 4260880, 67372036, 8521760, 134744072, 17043520, 2155905152, 272696320, 4311810304, 545392640, 8623620608, 1090785280, 17247241216, 2181570560, 275955859456, 34905128960, 551911718912, 69810257920, 1103823437824, 139620515840, 2207646875648, 279241031680]   
win_conds = sorted(win_conds)

# we can deduce columns with bitboard math as well:
# popcnt of col & board = number of pieces in that board
cols = [2216338399296, 1108169199648, 554084599824, 277042299912, 138521149956, 69260574978, 34630287489]

# according to here: http://www.valuedlessons.com/2009/01/popcount-in-python-with-benchmarks.html
# this is the fastest way to do a popcnt in python with the number of bits i need
popcountmemo = {}
def popcount(v):
    original = v
    if v not in popcountmemo:
        c = 0
        while v:
            v &= v - 1
            c += 1
        popcountmemo[original] = c
    return popcountmemo[original]

class Root_Node:
    def __init__(self):
        # initialize the bitboards for each side
        self.board = [0,0]
        self.value = 0
        self.side_to_move = True

    def gethash(self):
        return str(self.board)

    def update(self, position): # takes a position from the engine and updates our internal position
        for i in range(6):
            for j in range(7):
                value = ((6 - j) + ((5 - i) * 7))
                space = 2**value
                if self.value & space == 0 and position[value] in ['1', '2']:
                    self.make(6 - j)
        return 6 - j

    def turn(self):
        return (self.side_to_move * 2 - 1)

    def col_height(self, column):
        return popcount(cols[column] & self.value)

    # makes a move in a column
    def make(self, column):
        self.board[self.side_to_move] |= (2**(6-column))*2**(7*self.col_height(column))
        self.side_to_move = not self.side_to_move
        self.value = self.board[0] | self.board[1]

    # unmakes a move in a column (subtract one from column height to get the correct move)
    def unmake(self, column):
        self.side_to_move = not self.side_to_move
        self.board[self.side_to_move] ^= (2**(6-column))*2**(7*(max(self.col_height(column) - 1, 0)))
        self.value = self.board[0] | self.board[1]

    # takes a power of two (a single square) and checks if the square below it is empty or not
    def is_hanging(self, square):
        return not (square / 2**7) & self.value

    # generates all of the legal moves in a position
    def move_gen(self):
        return sorted([x for x in range(7) if cols[x] & (self.value) != cols[x]], key=lambda k: abs(3 - k))
    
    def score(self):
        score = 0

        # iterate over win conds to find threats and check for wins
        immeadiate_threats = []
        hanging_threats = []
        for i in win_conds:
            if i > self.value:
                break
            # side to move == 1 goes first, so board[1]
            red = self.board[0] & i
            blue = self.board[1] & i
            if red == i or blue == i:
                # someone just won, return a score thats bad for the side to move
                return -10000 * self.turn()
            if blue == 0 and popcount(red) == 3:
                threat = red ^ i * -1
                if not self.is_hanging(threat):
                    immeadiate_threats.append(threat)
                    if not self.side_to_move:
                        return -9999
                else:
                    hanging_threats.append(threat)
            elif red == 0 and popcount(blue) == 3:
                threat = blue ^ i
                if not self.is_hanging(threat):
                    immeadiate_threats.append(threat)
                    # theat is > 0 so we just check if self.side_to_move, since not self.side_to_move just blundered
                    if self.side_to_move:
                        return 9999
                else:
                    hanging_threats.append(threat)

        blanks = popcount(self.value)

        threats = immeadiate_threats + hanging_threats

        score += len(filter(lambda x: x > 0, threats))
        score -= score - len(threats)

        return score
                
    def display_board(self):
        for i in range(6):
            for j in range(7):
                space = 2**((6 - j) + ((5 - i) * 7))
                if self.board[0] & space == space:
                    print("-1, ", end="")
                elif self.board[1] & space == space:
                    print("01, ", end="")
                else:
                    print("00, ", end="")
            print("")

myBook = book()

if __name__ == "__main_1_" :
    connectfour = Search(Root_Node())
    connectfour.settings['current_time'] = 10000
    connectfour.settings['timebank'] = 10000
    connectfour.settings['time_per_move'] = 500
    connectfour.settings['round'] = 1   
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
        if processed[0] == "exit":
            quit()
        if processed[0] == "update":
            if processed[1] == "game":
                if processed[2] == "field":
                    move = connectfour.root.update(processed[3].replace(";", ",").split(","))
                    connectfour.line += str(move)
                if processed[2] == "round":
                    connectfour.set_setting(processed[2], processed[3])
                connectfour.set_setting(processed[1], processed[2])
        if processed[0] == "action":
            if myBook.inBook(connectfour.line):
                stderr.write("Book Move: %s\n" % (myBook.getMove(connectfour.line)))
                stderr.flush()
                stdout.write("place_disc %s \n" % (myBook.getMove(connectfour.line)))
                stdout.flush()
                connectfour.root.make(int(myBook.getMove(connectfour.line)))
                connectfour.line += myBook.getMove(connectfour.line)
            else:
                start = time.time()
                connectfour.set_setting("current_time", processed[2])
                move = connectfour.go()
                stdout.write("place_disc %s \n" % (move))
                connectfour.line += str(move)
                stdout.flush()
                stderr.write("Searched %s nodes in %s seconds \n" % (str(connectfour.nodes), str(time.time() - start)))
                stderr.flush()
            stderr.write("Completed Round: " + str(connectfour.settings["round"]) + "\n")
            stderr.write("Line: " + connectfour.line + "\n")
            stderr.flush()
            
if __name__ == "__main__" :
    connectfour = Search(Root_Node())
    while True:
        connectfour.root.display_board()
        connectfour.nodes = 0
        move = int(raw_input())
        connectfour.root.make(move)
        connectfour.line += str(move)
        connectfour.settings['current_time'] = 100000
        connectfour.settings['timebank'] = 100000
        connectfour.settings['time_per_move'] = 5000
        connectfour.settings['round'] = 1
        if myBook.inBook(connectfour.line):
            stderr.write("Book Move: %s\n" % (myBook.getMove(connectfour.line)))
            stderr.flush()
            stdout.write("place_disc %s \n" % (myBook.getMove(connectfour.line)))
            stdout.flush()
            connectfour.root.make(int(myBook.getMove(connectfour.line)))
            connectfour.line += myBook.getMove(connectfour.line)
        else:  
            start = time.time()
            connectfour.go()
            print("searched %s nodes in %s seconds" % (str(connectfour.nodes), str(time.time() - start)))


