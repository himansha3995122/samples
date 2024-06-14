from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D


class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation (Alternative Version).
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
        current_cell = entrance

        while current_cell not in maze.getExits():
            next_cell = self.getNextCell(current_cell, direction)

            if maze.hasCell(next_cell) and not maze.hasWall(current_cell, next_cell):
                self.solverPathAppend(next_cell, False)
                current_cell = next_cell
                turn_count = 0
            else:
                direction = (direction + self.turns[turn_count % 4]) % 4
                turn_count += 1
                self.solverPathAppend(current_cell, True)
                if turn_count > len(self.turns) * 2:
                    break

        if current_cell in maze.getExits():
            self.solved(entrance, current_cell)
        else:
            self.m_entranceUsed = entrance
            self.m_exitUsed = current_cell

    def getNextCell(self, cell: Coordinates3D, direction: int) -> Coordinates3D:
        row_offset, col_offset = self.directions[direction]
        return Coordinates3D(
            cell.getLevel(), cell.getRow() + row_offset, cell.getCol() + col_offset
        )
