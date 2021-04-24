from typing import List, Tuple

# Using constants might make this more readable.
START = 'S'
EXIT = 'X'
VISITED = '.'
OBSTACLE = '#'
PATH = ' '


class Maze:
    """Maze object, used for demonstrating recursive algorithms."""

    def __init__(self, maze_str: str):
        """Initialize Maze.

        Args:
            maze_str (str): Maze represented by a string, 
            where rows are separated by newlines (\\n).

        Raises:
            ValueError, if maze_str is invalid, i.e. if it is not the correct type, 
            if any of its dimensions is less than three, or if it contains 
            characters besides {'\\n', ' ', '*'}.
        """
        # We internally treat this as a List[List[str]], as it makes indexing easier.
        self._maze = list(list(row) for row in maze_str.splitlines())

        self._exits: List[Tuple[int, int]] = []
        self._max_recursion_depth = 0

    def find_exits(self, start_x: int, start_y: int, depth: int = 0) -> None:
        """Find and save all exits into `self._exits` using recursion, save 
        the maximum recursion depth into 'self._max_recursion_depth' and mark the maze.

        An exit is an accessible from S empty cell on the outer rims of the maze.

        Args:
            start_x (int): x-coordinate to start from. 0 represents the topmost cell.
            start_y (int): y-coordinate to start from; 0 represents the leftmost cell.
            depth (int): Depth of current iteration.

        Raises:
            ValueError: If the starting position is out of range or not walkable path.
        """
        # Starting position out of range
        if start_x > len(self._maze) - 1 or start_y > len(self._maze[0]) - 1 or start_y < 0 or start_x < 0:
            if depth == 0:
                raise ValueError
            else:
                return False

        # Position is obstacle
        if self._maze[start_x][start_y] == OBSTACLE:
            if depth == 0:
                raise ValueError
            else:
                return False

        if depth == 0:
            # at the beginning, mark START
            self._maze[start_x][start_y] = START
            # CASE: start is exit
            if (start_y == 0 or start_y == len(self._maze[0]) - 1 or
                    start_x == 0 or start_x == len(self._maze) - 1):  # if true, we are at the edge of the maze --> exit
                if self._maze[start_x][start_y] == START:
                    self._exits.append((start_x, start_y))
                    self._maze[start_x][start_y] = EXIT

        depth += 1  # increase current depth
        if depth > self._max_recursion_depth:
            self._max_recursion_depth = depth

        # CASE: Starting position is EXIT
        # --> try to get out; moving into all directions
        # can only happen for one position
        if self._maze[start_x][start_y] == EXIT and depth == 1:
            if self.find_exits(start_x - 1, start_y, depth):  # NORTH
                return True
            elif self.find_exits(start_x + 1, start_y, depth):  # SOUTH
                return True
            elif self.find_exits(start_x, start_y - 1, depth):  # WEST
                return True
            elif self.find_exits(start_x, start_y + 1, depth):  # EAST
                return True
            elif self.find_exits(start_x - 1, start_y + 1, depth):  # NORTHEAST
                return True
            elif self.find_exits(start_x - 1, start_y - 1, depth):  # NORTHWEST
                return True
            elif self.find_exits(start_x + 1, start_y + 1, depth):  # SOUTHEAST
                return True
            elif self.find_exits(start_x + 1, start_y - 1, depth):  # SOUTHWEST
                return True

        # If close to EXIT, try to find EXIT
        # SOUTH
        if len(self._maze) - 2 == start_x:  # we are possibly one position BELOW the EXIT
            if self._maze[start_x + 1][start_y] == PATH:
                self._exits.append((start_x + 1, start_y))
                self._maze[start_x + 1][start_y] = EXIT

        # NORTH
        if start_x == 1:  # we are possibly one position ABOVE the EXIT
            if self._maze[start_x - 1][start_y] == PATH:
                self._exits.append((start_x - 1, start_y))
                self._maze[start_x - 1][start_y] = EXIT

        # WEST
        if start_y == 1:  # we are possibly one position to the RIGHT of the EXIT
            if self._maze[start_x][start_y - 1] == PATH:
                self._exits.append((start_x, start_y - 1))
                self._maze[start_x][start_y - 1] = EXIT

        # EAST
        if len(self._maze[0]) - 2 == start_y:  # we are possibly one position to the LEFT of the EXIT
            if self._maze[start_x][start_y + 1] == PATH:
                self._exits.append((start_x, start_y + 1))
                self._maze[start_x][start_y + 1] = EXIT

        # BASE CASES
        if self._maze[start_x][start_y] == OBSTACLE or self._maze[start_x][start_y] == EXIT:
            return False
        elif self._maze[start_x][start_y] == VISITED and not (self._maze[start_x][start_y] == START):
            return False

        # mark current position as VISITED
        # make sure not to overwrite START or EXIT
        if not (self._maze[start_x][start_y] == START) and not (self._maze[start_x][start_y] == EXIT):
            # to account for 'broad exits', i.e., >= 2 exits next to each other
            if (self._maze[start_x][start_y] == ' ') and \
                    (start_y == 0 or start_x == 0 or
                     len(self._maze) - 1 == start_x or len(self._maze[0]) - 1 == start_y):
                self._exits.append((start_x, start_y))
                self._maze[start_x][start_y] = EXIT
            else:
                self._maze[start_x][start_y] = VISITED

        # CHANGE POSITION recursively, one after another
        # remembering old position when going back using recursion
        if self.find_exits(start_x - 1, start_y, depth):  # NORTH
            return True
        if self.find_exits(start_x + 1, start_y, depth):  # SOUTH
            return True
        if self.find_exits(start_x, start_y + 1, depth):  # EAST
            return True
        if self.find_exits(start_x, start_y - 1, depth):  # WEST
            return True
        if self.find_exits(start_x - 1, start_y + 1, depth):  # NORTHEAST
            return True
        if self.find_exits(start_x - 1, start_y - 1, depth):  # NORTHWEST
            return True
        if self.find_exits(start_x + 1, start_y + 1, depth):  # SOUTHEAST
            return True
        if self.find_exits(start_x + 1, start_y - 1, depth):  # SOUTHWEST
            return True
        return False

    @property
    def exits(self) -> List[Tuple[int, int]]:
        """List of tuples of (x, y)-coordinates of currently found exits."""
        return self._exits

    @property
    def max_recursion_depth(self) -> int:
        """Return the maximum recursion depth after executing find_exits()."""
        return self._max_recursion_depth

    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self._maze)

    __repr__ = __str__
