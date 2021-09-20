DECIMAL = 3

class Point:
    ON_STR = 'M3'
    OFF_STR = 'M5'

    def __init__(self, y: int, state: bool):
        self.y = y
        self.state = state

    def __str__(self):
        return self.code(1.0)

    def code(self, step: float) -> str:
        return f'Y{round(self.y * step, DECIMAL):.{DECIMAL}f}\n{self.ON_STR if self.state else self.OFF_STR}\n'

class Line:
    def __init__(self, x, data):
        self.x = x
        self.set_points(data)

    def empty(self):
        return not bool(len(self.points))

    def _add_point(self, y, state):
        self.points.append(Point(y, state))
        return not state

    def set_points(self, points):
        self.points = []
        state = False
        for y, p in enumerate(reversed(points)):
            if (state and p == 255) or (not state and p == 0):
                state = self._add_point(len(points) - 1 - y, state)
        for y, p in enumerate(points):
            if (state and p == 255) or (not state and p == 0):
                state = self._add_point(y, state)
        if state:
            self._add_point(len(points) - 1, False)

    def x_code(self, step):
        return f'X{round(self.x * step, 3):.3f}\n'

    def code(self, step):
        result = []
        result.append(self.x_code(step))
        if self.dir:
            for p in self.points:
                result.append(p.code())
        else:
            for p in reversed(self.points):
                result.append(p.code())

    def __str__(self):
        return f'({self.min}, {self.max})'

class Layer:
    def __init__(self, z, data, width, start_x=0, start_y=0):
        self.z = z
        self.start_x = start_x
        self.start_y = start_y
        self.set_lines(data, width)

    def set_lines(self, data, width):
        self.lines = []
        reverse = False
        for x, i in enumerate(range(0, len(data), width)):
            line = Line(x, data[i:i + width], reverse)
            if line.empty():
                continue
            self.lines.append(line)
            reverse = not reverse

    def set_start(self, x, y):
        self.start_x = x
        self.start_y = y

    def __str__(self):
        return f'Layer Z: {self.z}'
