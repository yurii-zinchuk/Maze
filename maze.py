"""Implemention of the Maze ADT using a 2-D array."""
from arrays import Array2D
from lliststack import Stack


class Maze:
    """Define constants to represent contents of the maze cells."""
    MAZE_WALL = "*"
    PATH_TOKEN = "x"
    TRIED_TOKEN = "o"

    def __init__(self, num_rows, num_cols):
        """Creates a maze object with all cells marked as open."""
        self._maze_cells = Array2D(num_rows, num_cols)
        self._start_cell = None
        self._exit_cell = None

    def num_rows(self):
        """Returns the number of rows in the maze."""
        return self._maze_cells.num_rows()

    def num_cols(self):
        """Returns the number of columns in the maze."""
        return self._maze_cells.num_cols()

    def set_wall(self, row, col):
        """Fills the indicated cell with a "wall" marker."""
        assert row >= 0 and row < self.num_rows() and \
            col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._maze_cells[row, col] = self.MAZE_WALL

    def set_start(self, row, col):
        """Sets the starting cell position."""
        assert row >= 0 and row < self.num_rows() and \
            col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._start_cell = _CellPosition(row, col)

    def set_exit(self, row, col):
        """Sets the exit cell position."""
        assert row >= 0 and row < self.num_rows() and \
            col >= 0 and col < self.num_cols(), "Cell index out of range."
        self._exit_cell = _CellPosition(row, col)

    def find_path(self):
        """
        Attempts to solve the maze by finding a path from the starting cell
        to the exit. Returns True if a path is found and False otherwise.
        """
        position = _CellPosition(self._start_cell.row, self._start_cell.col)
        move_stack = Stack()
        move_stack.push((0, 0))
        visited = {(position.row, position.col)}
        while not move_stack.is_empty():
            coords = [(position.row, position.col-1), (position.row+1, position.col),
                      (position.row, position.col+1), (position.row-1, position.col)]
            isolated = True
            for coord in coords:
                if self._valid_move(*coord):
                    isolated = False
                    move_stack.push(coord)
            next_pos = move_stack.pop()
            if isolated:
                self._mark_tried(position.row, position.col)
            else:
                self._mark_path(position.row, position.col)
            visited.add(next_pos)
            position = _CellPosition(*next_pos)
            if self._exit_found(*next_pos):
                self._mark_path(*next_pos)
                return True
        self.reset()
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                if self._valid_move(i, j):
                    self._mark_tried(i, j)


    def reset(self):
        """Resets the maze by removing all "path" and "tried" tokens."""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                if self._maze_cells[i, j] == self.TRIED_TOKEN or \
                        self._maze_cells[i, j] == self.PATH_TOKEN:
                    self._maze_cells[i, j] = None

    def __str__(self):
        """Returns a text-based representation of the maze."""
        result = ""
        for i in range(self.num_rows()):
            for j in range(self.num_cols()):
                result += self._maze_cells[i, j]+" " if self._maze_cells[i, j] else "_ "
            result += "\n"
        with open("str.txt", "w") as file:
            file.write(result[:-1])
        return result[:-1]

    def _valid_move(self, row, col):
        """Returns True if the given cell position is a valid move."""
        return row >= 0 and row < self.num_rows() \
            and col >= 0 and col < self.num_cols() \
            and self._maze_cells[row, col] is None

    def _exit_found(self, row, col):
        """Helper method to determine if the exit was found."""
        return row == self._exit_cell.row and col == self._exit_cell.col

    def _mark_tried(self, row, col):
        """Drops a "tried" token at the given cell."""
        self._maze_cells[row, col] = self.TRIED_TOKEN

    def _mark_path(self, row, col):
        """Drops a "path" token at the given cell."""
        self._maze_cells[row, col] = self.PATH_TOKEN


class _CellPosition(object):
    """Private storage class for holding a cell position."""

    def __init__(self, row, col):
        self.row = row
        self.col = col
