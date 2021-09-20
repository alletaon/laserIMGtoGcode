from laser import Line

def test_line_init():
    line = Line(0, [255] * 10, False)
    assert line.x == 0
    assert line.points == []
