from sys import stderr, stdin, stdout
import time, random
from copy import deepcopy

# we hit search explosion 19 ply before the end
SEARCH_EXPLOSION = 19

class Search:
    def __init__(self, root):

        self.start_time = 0
        
        self.settings = {}
        self.nodes = 0
        self.leaves = 0
        self.root = root
        self.tt = {} # WOOT Transposition table! {boardstring: [depth, score]}
        self.history = {} # History uses negative values to avoid reversing the list

        self.allowed_time = None
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
        if current_round >= 42 - SEARCH_EXPLOSION:
            return current_time / 1000.0
        thinking_time = (current_time + increment * 0.5 *(42 - (current_round + SEARCH_EXPLOSION))) / ((42 - SEARCH_EXPLOSION - current_round) * 0.5)
        #print("Total timeback left: " + str(current_time + increment * 0.5 *(42 - (current_round + SEARCH_EXPLOSION))))
        #print("Total Rounds left: " + str(((42 - SEARCH_EXPLOSION - current_round) * 0.5)))
        return min(thinking_time, current_time) / 1000.0
    def pick_best(self, candidate, best, side_to_move):
        if (candidate > best and side_to_move == 1) or (candidate < best and side_to_move == -1):
            return candidate
        return best
    
    def minimax(self, depth, alpha, beta):
        self.nodes += 1
        oldBest = None

        if self.allowed_time - (time.time() - self.start_time) < 0.05:
            raise RuntimeError("Out of time!")
        
        if self.root.gethash() in self.tt:
            if self.tt[self.root.gethash()][1] == depth:
                return self.tt[self.root.gethash()][0]
            oldBest = self.tt[self.root.gethash()][2]

        myScore = self.root.score()
        if depth == 0 or abs(myScore) == 10000 or len(self.root.move_gen()) == 0:
            self.leaves += 1
            return myScore
        bestValue = 10001 * -1 * self.root.turn()
        moveset = sorted(self.root.move_gen(), key=lambda k: self.history[(k, depth)])
        if oldBest is not None and oldBest in moveset:
            moveset.remove(oldBest)
            moveset.insert(0, oldBest)
        # set our bestmove to none and update it as we search
        best = moveset[0]
        for child in moveset:
            
            self.root.make(child)
            
            search = self.minimax(depth - 1, alpha, beta)
            # Turns are all swapped because make changed the turn...
            bestValue = self.pick_best(search, bestValue, self.root.turn() * -1)
            if self.root.turn() == -1 and bestValue > alpha:
                alpha = bestValue
                best = child
            elif self.root.turn() == 1 and bestValue < beta:
                beta = bestValue
                best = child
                
            self.root.unmake(child)
            if beta <= alpha:
                self.history[(child, depth)] -= 1
                break
        self.tt[self.root.gethash()] = (bestValue, depth, best)
        return bestValue
                
    
    def go(self):
        # clear the tt before starting a search also clear stats
        #self.tt = {}
        self.start_time = time.time()
        self.nodes = 0
        self.leaves = 0
        self.clear_history()

        self.allowed_time = self.current_move_time()

        stderr.write("Thinking time: " + str(self.current_move_time()) + "\n")

        bestMove = None

        score = 0
        backup = deepcopy(self.root)
        depth = 0
        while True:
            #try:
                depth += 1
                score = self.minimax(depth, -999999, 999999)
                stderr.write("[INFO] depth %s score %s \n" % (str(depth), score))
                bestMove = self.tt[self.root.gethash()][2]
                stderr.flush()
            #except:
            #    break
            
        self.root = backup
        self.root.make(bestMove)
        return bestMove
