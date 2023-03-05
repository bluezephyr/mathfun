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

    def toggle_window(self, window_nbr):
        if window_nbr < 1 or window_nbr > self._nof_windows:
            return
        self._windows[window_nbr] = not self._windows[window_nbr]

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
            self._screen.addstr(y + 1, x + 1 + x_pad, str(number), YELLOW_TEXT | curses.A_REVERSE)
        else:
            self._screen.addstr(y + 1, x + 1 + x_pad, str(number), YELLOW_TEXT)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.curs_set(0)
    stdscr.clear()

    building = Building(stdscr, 10, 100)
    building.draw(0, 0)
    window = 0
    stdscr.addstr(building.height() + 1, 0, f"Current window number: {window}")
    stdscr.refresh()

    delta = 0
    while True:
        key = stdscr.getkey()
        if key == "KEY_LEFT":
            delta = -1
        elif key == "KEY_RIGHT":
            delta = 1
        elif key == "q":
            break
        else:
            delta = 0
        window += delta
        if window < 1:
            window = 1
        if window > 100:
            window = 100

        building.toggle_window(window)
        stdscr.clear()
        building.draw(0, 0)
        stdscr.addstr(building.height() + 1, 0, f"Current window number: {window}")
        stdscr.addstr(building.height() + 2, 0, "Enter window number: ")
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
