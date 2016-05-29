import time, random
from board import Root_Node

def test_speed():
    print("")
    for x in range(0, 3):
        foo = Root_Node()
        start = time.time()
        counter = 0
        while time.time() - start < 1:
            counter += 1
            if len(foo.legal_moves()) == 0 or foo.won:
                foo = Root_Node()
            else:
                foo.export()
                foo.make_move(random.choice(foo.legal_moves()))
                foo.score()
        print(counter)
        assert counter > 1000
def test_threats_simple():
    foo = Root_Node()
    foo.make_move(0)
    foo.make_move(6)
    foo.make_move(1)
    foo.make_move(5)
    foo.make_move(2)
    assert 38 in foo.threats
    assert -38 not in foo.threats
    foo.make_move(4)
    assert -38 in foo.threats
    assert 38 in foo.threats
    foo.make_move(3)
    assert -38 not in foo.threats
    assert 38 not in foo.threats
def test_traverse():
    foo = Root_Node()
    bar = foo.traverse((1, 2), 6)
    assert next(bar) == (2, 3)
    assert next(bar) == (3, 4)
def test_square_validity():
    foo = Root_Node()
    assert not foo.is_valid((-1, 5))
    for i in range(0, 7):
        for x in range(0, 6):
            assert foo.is_valid((x, i))
def test_full_Game():
    foo = Root_Node()
    for i in "4444452322223353347777362177555511111":
        foo.make_move(int(i) - 1)
    assert foo.board == [[1, 1, 1, -1, -1, 0, -1], [-1, -1, 1, 1, 1, 0, 1], [1, 1, -1, -1, -1, 0, -1], [-1, -1, -1, 1, 1, 0, 1], [1, 1, 1, -1, 1, 0, -1], [-1, 1, -1, 1, -1, -1, 1]]
    assert foo.threats == set([26.0, -5.0, 12.0, -19.0])
def test_node_export():
    foo = Root_Node()
    foo.make_move(0)
    bar = foo.export()
    foo.make_move(0)
    foo.make_move(1)
    foo.make_move(1)
    foo.make_move(2)
    foo.make_move(2)
    assert bar.board != foo.board
    assert bar.runs != foo.runs
    assert bar.threats != foo.threats
    assert bar.side_to_move != foo.side_to_move
