from minimax import Search
from sys import stderr, stdin, stdout

if __name__ == "__main_1_" :
    connectfour = Search()
    # to prevent a test crash
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
            stdout.write("place_disc %s\n" % (connectfour.go()))
            stdout.flush()
            stderr.write("Searched %s nodes in %s seconds \n" % (str(connectfour.nodes), str(time.time() - start)))
            stderr.flush()
            


