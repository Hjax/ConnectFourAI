import win32gui, win32api, win32con, time, colorsys
from win32api import GetSystemMetrics
import ImageGrab
from connectfour import *
from minimax import *
from book import *
import threading

## TODO  HANDLE WHEN TWO STRIPES ARE THE SAME COLOR
##       MAKE METHOD FOR FINDING KEYS

start = [785, 135]
NUM_TABS = 20
tabs = [True] * NUM_TABS

lock = threading.Lock()

class grabber:
    def __init__(self):
        self.image = ImageGrab.grab()

    def capture(self):
        self.image = ImageGrab.grab()

    def get_pixel_color(self, i_x, i_y):
        return self.image.getpixel((i_x, i_y))

    def click(self, x,y):
            win32api.SetCursorPos((x,y))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    def get_board(self):
        columns = [0,0,0,0,0,0,0]
        for i in range(0, 6):
            for j in range(0, 7):
                if self.get_pixel_color(start[0] + 135 * j, start[1] + 135 * i) != (255, 255, 255):
                    columns[j] += 1
        return columns

    def enter_board_string(self, board):
        for i in board:
            self.click(start[0] + 135 * int(i), 135)

    def click_back(self):
        self.click(475, 780)

    def reset(self):
        for i in range(0, 20):
            self.click_back()

    def enter_next_move(self):
        if self.get_pixel_color(585, 875) == (166, 165, 201):
            self.click(585, 875)
            self.click(585, 875)
        else:
            self.click(585, 975)
            self.click(585, 975)

    def get_best_move(self, board_string):
        self.reset()
        self.enter_board_string(board_string)
        time.sleep(0.7)
        first = self.get_board()
        self.enter_next_move()
        time.sleep(0.7)
        second = self.get_board()
        for i in range(0, 7):
            if first[i] != second[i]:
                return i
        return -1

    def get_tab(self):
        while True:
            lock.acquire()
            for i in range(len(tabs)):
                if tabs[i]:
                    tabs[i] = False
                    lock.release()
                    return i
            lock.release()
            time.sleep(0.1)

    def release_tab(self, tab):
        lock.acquire()
        tabs[tab] = True
        lock.release()

    def switch_tab(self, tab):
        self.click(50 + 83*tab, 15)
        time.sleep(0.05)
            

transpose = []
bk = book()
bk.book = {}

found = 0

def generate(node, max_depth, printer=False):
    global found
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
    if abs(checker.minimax(node, 4, -999999, 999999)) > 5000:
        #print("Aborting line due to bad score")
        return
    transpose.append(node.gethash())
    # get the best move for this position
    #bk.book[node.line] = str(foo.get_best_move(node.line))
    lock.acquire()
    if node.line not in bk.opening_book:
        print(found)
        found += 1
        bk.book[node.line] = ""
    lock.release()
    for move in node.legal_moves():
        if printer:
            print(move)
        child = node.export()
        child.make_move(move)
        generate(child, max_depth - 1)

def do_sleep():
    lock.release()
    time.sleep(1.1)
    lock.acquire()

def worker():
    foo = grabber()
    while True:

        my_tab = foo.get_tab()
        my_key = ""

        while my_key == "":
            lock.acquire()
            for key in bk.book:
                if bk.book[key] == "":
                    my_key = key
                    bk.book[key] = "taken"
                    break
            lock.release()
            time.sleep(0.05)
        lock.acquire()

        foo.switch_tab(my_tab)
        foo.reset()
        foo.enter_board_string(my_key)
        do_sleep()
        foo.switch_tab(my_tab)
        time.sleep(0.1)
        foo.capture()
        lock.release()
        first = foo.get_board()
        lock.acquire()
        foo.switch_tab(my_tab)
        foo.enter_next_move()
        do_sleep()
        foo.switch_tab(my_tab)
        time.sleep(0.1)
        foo.capture()
        lock.release()
        second = foo.get_board()
        for i in range(0, 7):
            if first[i] != second[i]:
                lock.acquire()
                bk.book[my_key] = str(i)
                lock.release()
        foo.release_tab(my_tab)


threads = []
for i in range(0, NUM_TABS):
    threads.append(threading.Thread(target=worker))
    threads[i].daemon = True
    threads[i].start()

startt = time.time()
generate(Root_Node(), 7, True)

while True:
    time.sleep(1)
    lock.acquire()
    done = True
    counter = 0
    for key in bk.book:
        if bk.book[key] == "" or bk.book[key] == "taken" and key != "":
            counter += 1
            done = False
    lock.release()
    print(counter)
    if done:
        break
    
print(time.time() - startt)
print(len(bk.book))

filer = open("output.txt", "w")
filer.write(str(bk.book))
filer.close()
