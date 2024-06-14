from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from random import choice


class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up
        self.turns = [1, -1, 1, -1]  # right turn = +1, left turn = -1

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        self.resetPathAndCellExplored()

        direction = 0
        turn_count = 0
        curr_cell = entrance

        while curr_cell not in maze.getExits():
            next_cell = self.getNextCell(curr_cell, direction)

            if maze.hasCell(next_cell) and not maze.hasWall(curr_cell, next_cell):
                self.solverPathAppend(next_cell, False)
                curr_cell = next_cell
                turn_count = 0
            else:
                direction = (direction + self.turns[turn_count % 4]) % 4
                turn_count += 1
                self.solverPathAppend(curr_cell, True)
                if turn_count > len(self.turns) * 2:  # Prevent infinite loop
                    break

        if curr_cell in maze.getExits():
            self.solved(entrance, curr_cell)
        else:
            self.m_entranceUsed = entrance
            self.m_exitUsed = curr_cell

    def getNextCell(self, cell: Coordinates3D, direction: int) -> Coordinates3D:
        row_offset, col_offset = self.directions[direction]
        return Coordinates3D(
            cell.getLevel(), cell.getRow() + row_offset, cell.getCol() + col_offset
        )
