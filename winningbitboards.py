horizontal_base = 0b0001111
vertical_base = 0b1000000100000010000001
diag_left_base = 0b1000000010000000100000001
diag_right_base = 0b1000001000001000001000

horizontal_bases = []
for i in range(6):
    for j in range(4):
        horizontal_bases.append(horizontal_base)
        horizontal_base *= 2
    horizontal_base *= 2**4
    
vertical_bases = []
for i in range(21):
    vertical_bases.append(vertical_base)
    vertical_base *= 2

diag_bases = []
for i in range(3):
    for j in range(4):
        diag_bases.append(diag_left_base)
        diag_bases.append(diag_right_base)
        diag_left_base *= 2
        diag_right_base *= 2
    diag_left_base *= 2**4
    diag_right_base *= 2**4

bases = horizontal_bases + vertical_bases + diag_bases

def newLineSplit(string):
    n = 7
    chunks = [string[i:i+n] for i in range(0, len(string), n)]
    for i in chunks:
        print(i)
    print ""

for i in bases:
    thing = bin(i)[2:].zfill(42)
    if len(thing) != 42:
        print(thing)
        if i in vertical_bases:
            print "v"
        if i in horizontal_bases:
            print "h"
        if i in diag_bases:
            print "d"
            
    #newLineSplit()
    
