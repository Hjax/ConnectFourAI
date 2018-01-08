from connectfour import *
from minimax import *
from book import *

## TODO  HANDLE WHEN TWO STRIPES ARE THE SAME COLOR
##       MAKE METHOD FOR FINDING KEYS


transpose = []
count = 0
bk = book()
mybook = {}

def generate(node, max_depth, printer=False):
    global count
    
    if max_depth <= 0:
        return
    if node.gethash() in transpose:
        return
    if bk.inBook(node.line):
        return
    # if this position isnt useful, give up
    checker = Search(node)
    checker.clear_history()
    checker.allowed_time = 5
    checker.start_time = time.time()
    if abs(checker.minimax(node, 2, -999999, 999999)) > 5000:
        return
    transpose.append(node.gethash())
    # get the best move for this position
    #bk.book[node.line] = str(foo.get_best_move(node.line))
    mybook[node.line] = ""
    if (node.line not in bk.opening_book):
        count += 1
    for move in node.legal_moves():
        if printer:
            print(move)
        child = node.export()
        child.make_move(move)
        generate(child, max_depth - 1)



generate(Root_Node(), 7, True)
print(len(bk.opening_book))
print(len(mybook))
print(count)
