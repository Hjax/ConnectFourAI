from board import Root_Node
import time
from sys import stderr, stdin, stdout

from profilehooks import profile

class Search:
    def __init__(self):
        self.settings = {}
        self.start_time = 0
        self.nodes = 0
        self.leaves = 0
        self.root = Root_Node()
        self.tt = {} # WOOT Transposition table! {boardstring: [depth, score]}
        self.history = {} # History uses negative values to avoid reversing the list

        self.clear_history()
    def clear_history(self):
        for depth in range(0, 42):
            for move in range(0, 7):
                self.history[(move, depth)] = 0
    def age_history(self):
        for depth in range(0, 42):
            for move in range(0, 7):
                self.history[(move, depth - 1)] = self.history[(move, depth)]
    def set_setting(self, setting, value):
        self.settings[setting] = value
    def current_move_time(self): # returns the amount of time we are going to think for this move
        current_time = int(self.settings["current_time"])
        increment = int(self.settings["time_per_move"])
        current_round = int(self.settings["round"])
        if current_round == 42:
            return current_time
        return min(current_time / 1000.0, 1.4 * ((current_time + increment * (42 - current_round)) / (42 - current_round)) / 1000.0) - .05
    def minimax(self, node, depth, alpha, beta):

        if time.clock() - self.start_time > self.current_move_time():
            raise RuntimeError("Out of time")

        self.nodes += 1
        if node.gethash() in self.tt:
            if self.tt[node.gethash()][1] == depth:
                return self.tt[node.gethash()][0]
        if depth == 0 or abs(node.score()) == 10000 or len(node.legal_moves()) == 0:
            self.leaves += 1
            score = node.score() + (node.side_to_move * depth)
            self.tt[node.gethash()] = (score, depth, None)
            return score
        if node.side_to_move == 1:
            bestValue = -10001
        else:
            bestValue = 10001

        for child in sorted(node.legal_moves(), key=lambda k: self.history[(k, depth)]):
            current_child = node.export()
            current_child.make_move(child)
            search = self.minimax(current_child, depth - 1, alpha, beta)
            if node.side_to_move == 1:
                bestValue = max(search, bestValue)
                alpha = max(bestValue, alpha)
            else:
                bestValue = min(search, bestValue)
                beta = min(bestValue, beta)
            if beta <= alpha:
                self.history[(child, depth)] -= 1
                break
        self.tt[node.gethash()] = (bestValue, depth)
        return bestValue

    def go(self):
        # clear the tt before starting a search also clear stats
        self.tt = {}
        self.nodes = 0
        self.leaves = 0
        self.age_history()

        stderr.write("we have %s seconds for the current move\n" % (self.current_move_time()))
        self.start_time = time.clock()
        for depth in range(1, 42):
            stderr.write("[INFO] Depth: %s Nodes: %s\n" % (depth, self.nodes))
            stderr.flush()
            try:
                self.minimax(self.root, depth, -9999999, 9999999)
            except:
                stderr.write("hit time limit on iteration %s\n" % (str(depth)))
                stderr.flush()
                break
            
        best = (self.root.side_to_move * -99999999, None)
        scores = {}
        for move in self.root.legal_moves():
            new = self.root.export()
            new.make_move(move)
            scores[move] = self.tt[new.gethash()][0]
            if (self.root.side_to_move == 1 and self.tt[new.gethash()][0] > best[0]) or (self.root.side_to_move == -1 and self.tt[new.gethash()][0] < best[0]):
                best = [self.tt[new.gethash()][0], move]
        stderr.write(str(scores) + "\n")
        stderr.flush()
        self.root.make_move(best[1])
        return best[1]
