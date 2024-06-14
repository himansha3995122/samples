from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
from random import choice
from collections import deque


class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator with validation to ensure all cells are accessible.
    """

    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        start = Coordinates3D(0, 0, 0)
        maze_cells = {start}
        wall_list = [
            (start, neighbor)
            for neighbor in maze.neighbours(start)
            if maze.checkCoordinates(neighbor)
        ]

        while wall_list:
            current_wall = choice(wall_list)
            cell_a, cell_b = current_wall

            if cell_b not in maze_cells:
                maze_cells.add(cell_b)
                maze.removeWall(cell_a, cell_b)
                for neighbor in maze.neighbours(cell_b):
                    if neighbor not in maze_cells and maze.checkCoordinates(neighbor):
                        wall_list.append((cell_b, neighbor))

            wall_list.remove(current_wall)

        self._reinforceOuterWalls(maze)
        if not self._validateMaze(maze, start):
            print(
                "Validation failed, maze not fully accessible. Please regenerate the maze."
            )
        self.m_mazeGenerated = True

    def _validateMaze(self, maze, start):
        """Validate the maze to ensure all cells are reachable from the start."""
        visited = set()
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                for neighbor in maze.neighbours(current):
                    if (
                        not maze.hasWall(current, neighbor)
                        and neighbor in maze.allCells()
                    ):
                        queue.append(neighbor)
        # Check if the number of visited cells matches the total number of cells in the maze
        return len(visited) == sum(maze.cellNum(l) for l in range(maze.levelNum()))

    def _reinforceOuterWalls(self, maze):
        """Ensure the outer walls of the maze are intact."""
        for level in range(maze.levelNum()):
            for row in range(maze.rowNum(level)):
                maze.addWall(
                    Coordinates3D(level, row, 0), Coordinates3D(level, row, -1)
                )
                maze.addWall(
                    Coordinates3D(level, row, maze.colNum(level) - 1),
                    Coordinates3D(level, row, maze.colNum(level)),
                )
            for col in range(maze.colNum(level)):
                maze.addWall(
                    Coordinates3D(level, 0, col), Coordinates3D(level, -1, col)
                )
                maze.addWall(
                    Coordinates3D(level, maze.rowNum(level) - 1, col),
                    Coordinates3D(level, maze.rowNum(level), col),
                )


# This enhanced version of Prim's algorithm should help ensure that the maze is fully navigable, thereby reducing solver failures due to unreachable cells.
