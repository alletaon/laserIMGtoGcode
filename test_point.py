from laser import Point

def test_point_init():
    p = Point(1, False)
    assert p.y == 1
    assert p.state is False

def test_point_code():
    p1 = Point(10, True)
    p2 = Point(20, False)
    assert p1.code(1.0) == 'Y10.000\nM3\n'
    assert p2.code(1.0) == 'Y20.000\nM5\n'

def test_point_equal():
    p1 = Point(30, True)
    p2 = Point(30, True)
    assert p1 == p2

def test_point_not_equal():
    p1 = Point(40, True)
    p2 = Point(50, True)
    assert p1 != p2
    p3 = Point(40, False)
    assert p1 != p3
