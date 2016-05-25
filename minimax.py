from sys import stderr, stdin, stdout
import time, random
class Search:
    def __init__(self, root):

        self.start_time = 0
        
        self.settings = {}
        self.nodes = 0
        self.leaves = 0
        self.root = root
        self.tt = {} # WOOT Transposition table! {boardstring: [depth, score]}
        self.history = {} # History uses negative values to avoid reversing the list
    def clear_history(self):
        for depth in range(0, 20):
            for move in range(0, 7):
                self.history[(move, depth)] = 0
    def set_setting(self, setting, value):
        self.settings[setting] = value
    def current_move_time(self): # returns the amount of time we are going to think for this move
        max_time = int(self.settings["timebank"])
        current_time = int(self.settings["current_time"])
        increment = int(self.settings["time_per_move"])
        current_round = int(self.settings["round"])
        if current_round == 42:
            return current_time
        thinking_time = (current_time + increment * (42.0 - current_round)) / (42.0 - current_round)
        return thinking_time / 1000
    def pick_best(self, candidate, best, side_to_move):
        if (candidate > best and side_to_move == 1) or (candidate < best and side_to_move == -1):
            return candidate
        return best
    
    def minimax(self, node, depth, alpha, beta):
        self.nodes += 1
        oldBest = None

        if self.current_move_time() - (time.time() - self.start_time) < 0.05:
            raise RuntimeError("Out of time!")
        
        if node.gethash() in self.tt:
            if self.tt[node.gethash()][1] == depth:
                return self.tt[node.gethash()][0]
            oldBest = self.tt[node.gethash()][2]
        if depth == 0 or abs(node.score()) == 10000 or len(node.legal_moves()) == 0:
            self.leaves += 1
            return node.score()
        if node.side_to_move == 1:
            bestValue = -10001
        else:
            bestValue = 10000
        moveset = sorted(node.legal_moves(), key=lambda k: self.history[(k, depth)])
        if oldBest is not None and oldBest in moveset:
            moveset.remove(oldBest)
            moveset = [oldBest] + moveset
        # set our bestmove to none and update it as we search
        best = None
        for child in moveset:
            if best is None:
                best = child
            current_child = node.export()
            current_child.make_move(child)
            search = self.minimax(current_child, depth - 1, alpha, beta)
            bestValue = self.pick_best(search, bestValue, node.side_to_move)
            if node.side_to_move == 1 and bestValue > alpha:
                alpha = bestValue
                best = child
            elif node.side_to_move == -1 and bestValue < beta:
                beta = bestValue
                best = child
            if beta <= alpha:
                self.history[(child, depth)] -= 1
                break
        self.tt[node.gethash()] = (bestValue, depth, best)
        return bestValue
    
    def go(self):
        # clear the tt before starting a search also clear stats
        #self.tt = {}
        self.start_time = time.time()
        self.nodes = 0
        self.leaves = 0
        self.clear_history()

        depth = 0
        while True:
            try:
                depth += 1
                score = self.minimax(self.root, depth, -9999999, 9999999)
                stderr.write("[INFO] depth %s score %s \n" % (str(depth), score))
                stderr.flush()
            except:
                break
        PV = ""
        current = self.root.export()
        for i in range(0, 6):
            move = self.tt[current.gethash()][2]
            PV = PV + str(move) + ","
            current.make_move(move)
        stderr.write(PV + "\n")
        stderr.flush()
        self.root.make_move(self.tt[self.root.gethash()][2])
        return self.tt[self.root.gethash()][2]
