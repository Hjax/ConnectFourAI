from connectfour import *
import time

start = time.time()
count = 0


b = Root_Node()

while time.time() - start < 2:
    count += 1;
    b.make(0)
    b.col_height(0)
    b.unmake(0)

print(count)
