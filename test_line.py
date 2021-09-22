from laser import Line, Point

def test_line_init_empty():
    line = Line(0, [255] * 10, False)
    assert line.x == 0
    assert line.reverse is False
    assert line.points == []

def test_line_init():
    line1 = Line(1, [255, 255, 0, 255, 255], False)
    assert line1.points == [Point(2, True), Point(3, False)]
    line2 = Line(2, [0, 0, 0, 255, 255], False)
    assert line2.points == [Point(0, True), Point(3, False)]
    line3 = Line(3, [255, 255, 255, 255, 0], False)
    assert line3.points == [Point(4, True), Point(5, False)]
    line4 = Line(4, [0, 0, 0, 0, 0], False)
    assert line4.points == [Point(0, True), Point(5, False)]

def test_line_init_rev():
    line5 = Line(5, [255, 255, 0, 255, 255], True)
    assert line5.points == [Point(3, True), Point(2, False)]
    line6 = Line(6, [255, 255, 0, 0, 0], True)
    assert line6.points == [Point(5, True), Point(2, False)]
    line7 = Line(7, [0, 255, 255, 255, 255], True)
    assert line7.points == [Point(1, True), Point(0, False)]
    line8 = Line(8, [0, 0, 0, 0, 0], True)
    assert line8.points == [Point(5, True), Point(0, False)]

def test_line_code():
    line9 = Line(9, [255, 255, 0, 255, 255], False)
    assert line9.code(1.0) == ['X9.000', 'Y2.000', 'M3', 'Y3.000', 'M5']
    line10 = Line(10, [255, 255, 0, 255, 255], True)
    assert line10.code(1.0) == ['X10.000', 'Y3.000', 'M3', 'Y2.000', 'M5']
