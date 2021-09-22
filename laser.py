DECIMAL = 3

class Point:
    ON_STR = 'M62P0'
    OFF_STR = 'M63P0'

    def __init__(self, y: int, state: bool):
        self.y = y
        self.state = state

    def __str__(self):
        return f'Y: {self.y}, State: {self.s}'

    def __repr__(self) -> str:
        return f'{self.y}:{self.state}'

    def __eq__(self, o: object) -> bool:
        return self.y == o.y and self.state == o.state

    def code(self, step: float) -> 'list[str]':
        return [f'Y{round(self.y * step, DECIMAL):.{DECIMAL}f}', f'{self.ON_STR if self.state else self.OFF_STR}']

class Line:
    def __init__(self, x: int, data: 'list[int]', reverse: bool):
        self.x = x
        self.reverse = reverse
        self.set_points(data)

    def empty(self):
        return not bool(len(self.points))

    def _add_point(self, y, state):
        new_state = not state
        self.points.append(Point(y, new_state))
        return new_state

    def set_points(self, points: 'list[int]'):
        self.points = []
        state = False
        line = enumerate(reversed(points)) if self.reverse else enumerate(points)
        for i, p in line:
            if (state and p == 255) or (not state and p == 0):
                y = len(points) - i if self.reverse else i
                state = self._add_point(y, state)
        if state:
            if self.reverse:
                self._add_point(0, state)
            else:
                self._add_point(len(points), state)

    def x_code(self, step: float):
        return f'X{round(self.x * step, DECIMAL):.{DECIMAL}f}'

    def code(self, step: float) -> 'list[str]':
        result = []
        result.append(self.x_code(step))
        for p in self.points:
            result.extend(p.code(step))
        return result

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
