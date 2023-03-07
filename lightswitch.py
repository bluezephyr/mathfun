#!/usr/bin/python3
import curses
from curses.textpad import rectangle


WINDOWS_PER_FLOOR = 10
WINDOW_X_SPACE = 1
WINDOW_Y_SPACE = 1
WINDOW_X_PAD = 2
WINDOW_Y_PAD = 1
WINDOW_WIDTH = 4
WINDOW_HEIGHT = 2
ROOF_HEIGHT = 3
BUILDING_WIDTH = (
    WINDOWS_PER_FLOOR * (WINDOW_WIDTH + WINDOW_X_SPACE) + WINDOW_X_PAD * 2 - 1
)


class Building:
    def __init__(self, screen, floors, nof_windows):
        self._floors = floors
        self._nof_windows = nof_windows
        self._windows = {k + 1: False for k in range(nof_windows)}
        self._screen = screen
        self._x = 0
        self._y = 0

    def draw(self, x, y):
        self._x = x
        self._y = y
        self._draw_roof()
        self._draw_walls()
        for window_nbr in range(1, self._nof_windows + 1):
            self._draw_window(window_nbr)
        self._screen.refresh()

    def clear(self):
        self._windows = {k + 1: False for k in range(self._nof_windows)}

    def set_window_state(self, window_nbr, state):
        if window_nbr < 1 or window_nbr > self._nof_windows:
            return
        self._windows[window_nbr] = state

    def height(self):
        floors = self._nof_windows // WINDOWS_PER_FLOOR + (
            0 if self._nof_windows % WINDOWS_PER_FLOOR == 0 else 1
        )
        return self._y + ROOF_HEIGHT + floors * (WINDOW_HEIGHT + WINDOW_Y_PAD) + 1

    def _draw_roof(self):
        rectangle(self._screen, self._y, self._x, self._y, self._x + BUILDING_WIDTH - 2)
        self._screen.addstr(self._y + 0, self._x, "  /")
        self._screen.addstr(self._y + 1, self._x, " /")
        self._screen.addstr(self._y + 2, self._x, "/")
        self._screen.addstr(self._y + 0, self._x + BUILDING_WIDTH - 2, "\\")
        self._screen.addstr(self._y + 1, self._x + BUILDING_WIDTH - 2, " \\")
        self._screen.addstr(self._y + 2, self._x + BUILDING_WIDTH - 2, "  \\")

    def _draw_walls(self):
        rectangle(
            self._screen,
            self._y + ROOF_HEIGHT,
            self._x,
            self.height(),
            BUILDING_WIDTH,
        )

    def _draw_window(self, number):
        YELLOW_TEXT = curses.color_pair(1)
        x = (
            ((number - 1) % WINDOWS_PER_FLOOR) * (WINDOW_WIDTH + WINDOW_X_SPACE)
            + WINDOW_X_PAD
            + self._x
        )
        y = (
            ((number - 1) // WINDOWS_PER_FLOOR) * (WINDOW_HEIGHT + WINDOW_Y_SPACE)
            + ROOF_HEIGHT
            + WINDOW_Y_PAD
            + self._y
        )
        rectangle(self._screen, y, x, y + WINDOW_HEIGHT, x + WINDOW_WIDTH)
        x_pad = 1 if number < 10 else 0
        if self._windows[number]:
            self._screen.addstr(
                y + 1, x + 1 + x_pad, str(number), YELLOW_TEXT | curses.A_REVERSE
            )
        else:
            self._screen.addstr(y + 1, x + 1 + x_pad, str(number), YELLOW_TEXT)


class TextArea:
    def __init__(self, screen, y):
        self._y = y
        self._screen = screen
        self.switch = 0
        self.input = 0
        self.lit_windows = []

    def draw(self):
        self._screen.addstr(
            self._y + 1, 0, f"[{self.switch:3}] Enter switch number: {self.input}"
        )
        self._screen.addstr(self._y + 2, 0, f"{self.lit_windows}")
        self._screen.addstr(self._y + 3, 0, "Press 'C' to clear or 'Q' to quit")


class Switches:
    def __init__(self, nof_switches):
        self.switches = {k + 1: False for k in range(nof_switches)}

    def apply(self, switch):
        for i in range(1, switch + 1):
            self.switches[i] = not self.switches[i]
            # self.switches[i] = True


class Selector:
    def __init__(self, max_selection):
        self.input = ""
        self._value = 0
        self._value_updated = False
        self._max_selection = max_selection

    def _set(self, value):
        if value == self._value:
            return
        if value > self._max_selection:
            self._value = 0
        elif value < 0:
            self._value = self._max_selection
        else:
            self._value = value
        self._value_updated = True

    def get(self, key):
        self._value_updated = False
        if key == "KEY_LEFT":
            self._set(self._value - 1)
        elif key == "KEY_RIGHT":
            self._set(self._value + 1)
        elif key in "0123456789":
            self.input += key
        elif key == "KEY_BACKSPACE":
            self.input = self.input[:-1]
        elif key == "\n":
            if self.input:
                self._set(int(self.input))
                self.input = ""
        return self._value if self._value_updated else None


def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.clear()

    building = Building(stdscr, 10, 100)
    text_area = TextArea(stdscr, building.height())
    switches = Switches(100)
    selector = Selector(100)
    stdscr.refresh()

    while True:
        stdscr.clear()
        building.draw(0, 0)
        text_area.draw()
        stdscr.refresh()

        try:
            key = stdscr.getkey()
        except:
            key = ""

        if key in "Qq":
            break
        elif key in "Cc":
            building.clear()
        else:
            selection = selector.get(key)
            if selection:
                switches.apply(selection)
                text_area.switch = selection
                for window, state in switches.switches.items():
                    building.set_window_state(window, state)

        text_area.input = selector.input
        stdscr.addstr(
            building.height() + 2,
            0,
            f"{[k for k, v in switches.switches.items() if v]}",
        )


if __name__ == "__main__":
    curses.wrapper(main)
