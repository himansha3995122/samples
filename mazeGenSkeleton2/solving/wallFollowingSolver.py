from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from random import choice


class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        self.resetPathAndCellExplored()

        direction = 0
        curr_cell = entrance

        visited = set()
        visited.add(curr_cell)

        while curr_cell not in maze.getExits():
            right_dir = (direction + 1) % 4
            right_cell = self.getNextCell(curr_cell, right_dir)
            next_cell = self.getNextCell(curr_cell, direction)

            if maze.hasCell(right_cell) and not maze.hasWall(curr_cell, right_cell):
                direction = right_dir
                next_cell = right_cell
            elif not (
                maze.hasCell(next_cell) and not maze.hasWall(curr_cell, next_cell)
            ):
                direction = (direction - 1) % 4
                next_cell = self.getNextCell(curr_cell, direction)
                self.solverPathAppend(curr_cell, True)

            if next_cell in visited:
                break

            visited.add(next_cell)
            self.solverPathAppend(next_cell, False)
            curr_cell = next_cell

        if curr_cell in maze.getExits():
            self.solved(entrance, curr_cell)

    def getNextCell(self, cell: Coordinates3D, direction: int) -> Coordinates3D:
        row_offset, col_offset = self.directions[direction]
        return Coordinates3D(
            cell.getLevel(), cell.getRow() + row_offset, cell.getCol() + col_offset
        )
