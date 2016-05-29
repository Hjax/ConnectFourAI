from minimax import Search
from sys import stderr, stdin, stdout
import time

if __name__ == "__main__" :
    connectfour = Search()
    while True:
        connectfour.settings["time_per_move"] = 500
        connectfour.settings['current_time'] = 6000
        connectfour.settings['round'] = 35
        connectfour.root.display_board()
        connectfour.nodes = 0
        connectfour.root.make_move(int(input()))
        start = time.time()
        connectfour.go()
        print("searched %s nodes in %s seconds" % (str(connectfour.nodes), str(time.time() - start)))
