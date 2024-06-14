from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D


class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation (Alternative Version).
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # right, down, left, up

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        self.resetPathAndCellExplored()

        dir_index = 0
        current_pos = entrance
        visited_positions = {current_pos}

        while current_pos not in maze.getExits():
            right_index = (dir_index + 1) % 4
            right_pos = self.getNextCell(current_pos, right_index)
            next_pos = self.getNextCell(current_pos, dir_index)

            if maze.hasCell(right_pos) and not maze.hasWall(current_pos, right_pos):
                dir_index = right_index
                next_pos = right_pos
            elif not (
                maze.hasCell(next_pos) and not maze.hasWall(current_pos, next_pos)
            ):
                dir_index = (dir_index - 1) % 4
                next_pos = self.getNextCell(current_pos, dir_index)
                self.solverPathAppend(current_pos, True)

            if next_pos in visited_positions:
                break

            visited_positions.add(next_pos)
            self.solverPathAppend(next_pos, False)
            current_pos = next_pos

        if current_pos in maze.getExits():
            self.solved(entrance, current_pos)

    def getNextCell(self, cell: Coordinates3D, direction: int) -> Coordinates3D:
        row_offset, col_offset = self.directions[direction]
        return Coordinates3D(
            cell.getLevel(), cell.getRow() + row_offset, cell.getCol() + col_offset
        )
