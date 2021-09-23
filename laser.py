import math


DECIMAL = 3
ACCELERATION = 500

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
        return [f'Y{round(self.y * step, DECIMAL):.{DECIMAL}f}\n', f'{self.ON_STR if self.state else self.OFF_STR}\n']

class Line:
    def __init__(self, x: int, data: 'list[int]', reverse: bool):
        self.x = x
        self.reverse = reverse
        self.set_points(data)

    def empty(self):
        return len(self.points) == 0

    def _add_point(self, y, state):
        new_state = not state
        self.points.append(Point(y, new_state))
        return new_state

    def set_points(self, points: 'list[int]'):
        self.points = []
        state = False
        line = enumerate(reversed(points)) if self.reverse else enumerate(points)
        for i, p in line:
            if (state and p == 0) or (not state and p == 255):
                y = len(points) - i if self.reverse else i
                state = self._add_point(y, state)
        if state:
            if self.reverse:
                self._add_point(0, state)
            else:
                self._add_point(len(points), state)

        if self.points:
            if self.reverse:
                self.min = self.points[-1].y
                self.max = self.points[0].y
            else:
                self.min = self.points[0].y
                self.max = self.points[-1].y

    def get_lim(self) -> int:
        if self.reverse:
            return self.max
        return self.min

    def x_code(self, step: float):
        return f'X{round(self.x * step, DECIMAL):.{DECIMAL}f}\n'

    def code(self, step: float, allowance: float, nextLim: int, first: bool) -> 'list[str]':
        result = []
        result.append(self.x_code(step))
        if self.points and first:
            result.append(f'Y{round(self.min * step - allowance):.{DECIMAL}f}\n')
        for p in self.points:
            result.extend(p.code(step))
        if self.points and nextLim is not None:
            if self.reverse:
                result.append(f'Y{round(min(self.min, nextLim) * step - allowance):.{DECIMAL}f}\n')
            else:
                result.append(f'Y{round(max(self.max, nextLim) * step + allowance):.{DECIMAL}f}\n')
        return result

    def __str__(self):
        return f'{self.points}'

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

    def code(self, step: float, speed: int) -> 'list[str]':
        result = []
        allowance = speed**2 / (2 * ACCELERATION)    # S = V**2 / (2 * a), a = 500mm/s*s
        result.append('G64P0.1\n')
        result.append('G0X0Y0\n')
        result.append(f'G90G1F{speed * 60}\n')
        for i, line in enumerate(self.lines):
            lim = self.lines[i + 1].get_lim() if i < len(self.lines) - 1 else None
            result.extend(line.code(step, allowance, lim, i == 0))
        result.append('G0X0Y0\n')
        result.append('M30\n')
        return result

    def set_start(self, x, y):
        self.start_x = x
        self.start_y = y

    def estimate(self, speed, step):
        result = 0
        allowance = speed**2 / (2 * ACCELERATION)

        def calc(path):
            if path > allowance:
                return math.sqrt(2 * allowance / ACCELERATION) + (path - allowance) / speed
            return math.sqrt(2 * path / ACCELERATION)

        path_to_start = math.sqrt((self.lines[0].x * step)**2 + (self.lines[0].min * step)**2)
        result += calc(path_to_start)

        allowance_time = math.sqrt(2 * allowance / ACCELERATION)

        for i, line in enumerate(self.lines):
            result += (line.max - line.min) * step / speed
            result += 2 * allowance_time
            if i < len(self.lines) - 1:
                result += calc(self.lines[i + 1].x - line.x)

        path_from_end = math.sqrt((self.lines[-1].x * step)**2 + (self.lines[-1].max * step)**2)
        result += calc(path_from_end)
        return result

    def __str__(self):
        return f'Layer Z: {self.z}'
