from connectfour import *
from minimax import *
from book import *

## TODO  HANDLE WHEN TWO STRIPES ARE THE SAME COLOR
##       MAKE METHOD FOR FINDING KEYS


transpose = []
bk = book()
bk.book = {}

def generate(node, max_depth, printer=False):
    if max_depth <= 0:
        return
    if node.gethash() in transpose:
        #print("already have a transpose")
        return
    if bk.inBook(node.line):
        #print("already have symmertry")
        return
    # if this position isnt useful, give up
    checker = Search(node)
    checker.clear_history()
    checker.allowed_time = 5
    checker.start_time = time.time()
    if abs(checker.minimax(node, 2, -999999, 999999)) > 5000:
        #print("Aborting line due to bad score")
        return
    transpose.append(node.gethash())
    # get the best move for this position
    #bk.book[node.line] = str(foo.get_best_move(node.line))
    bk.book[node.line] = ""
    for move in node.legal_moves():
        if printer:
            print(move)
        child = node.export()
        child.make_move(move)
        generate(child, max_depth - 1)



generate(Root_Node(), 5, True)
print(len(bk.book))
