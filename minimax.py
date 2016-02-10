from sys import stderr, stdin, stdout
class Search:
    def __init__(self, root):
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
        thinking_time = (current_time + increment * (42 - current_round)) / (43 - current_round)
        return min(max(thinking_time, increment), current_time)
    def pick_best(self, candidate, _best, side_to_move):
        best = _best
        if (candidate[0] > best[0] and side_to_move == 1) or (candidate[0] < best[0] and side_to_move == -1):
            return candidate
        elif candidate[0] == best[0]:
            # if the score is good for the side to move, end the game sooner
            if (candidate[0] >= 0 and side_to_move == 1) or (candidate[0] <= 0 and side_to_move == -1):
                if len(candidate[1]) < len(best[1]):
                    return candidate
            else:
                if len(candidate[1]) > len(best[1]):
                    return candidate
        return best
    def minimax(self, node, depth, alpha, beta):
        self.nodes += 1
        cutoff = -1
        if node.gethash() in self.tt:
            if self.tt[node.gethash()][1] == depth:
                return self.tt[node.gethash()][0]
            else:
                cutoff = self.tt[node.gethash()][2]
        if depth == 0 or abs(node.score()) == 10000 or len(node.legal_moves()) == 0:
            self.leaves += 1
            return [node.score(), ""]
        if node.side_to_move == 1:
            bestValue = [-10001, ""]
        else:
            bestValue = [10000, ""]
        moveset = sorted(node.legal_moves(), key=lambda k: self.history[(k, depth)])
        if cutoff != -1:
            moveset.remove(cutoff)
            moveset = [cutoff] + moveset
        for child in moveset:
            current_child = node.export()
            current_child.make_move(child)
            search = self.minimax(current_child, depth - 1, alpha, beta)
            search[1] = str(child) + search[1]
            bestValue = self.pick_best(search, bestValue, node.side_to_move)[:]
            if node.side_to_move == 1:
                alpha = self.pick_best(bestValue, alpha, node.side_to_move)[:]
            else:
                beta = self.pick_best(bestValue, beta, node.side_to_move)[:]
            if beta[0] <= alpha[0]:
                self.history[(child, depth)] -= 1
                cutoff = child
                break
        self.tt[node.gethash()] = (bestValue[:], depth, cutoff)
        return bestValue
    def go(self):
        # clear the tt before starting a search also clear stats
        #self.tt = {}
        self.nodes = 0
        self.leaves = 0
        self.clear_history()
        best = None
        for depth in range(0, 8):
            best = self.minimax(self.root, depth, [-9999999, ""], [9999999, ""])
            stderr.write("[INFO] depth %s score %s \n" % (str(depth), str(best[0])))
            stderr.flush()
        stdout.write("place_disc %s \n" % (best[1][0]))
        stdout.flush()
        return best[1][0]
