# wilsonGenerator.py
# -------------------------------------------------------------------
# Wilson's algorithm maze generator (Alternative Version)
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
from random import choice


class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson's algorithm maze generator (Alternative Version).
    """

    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        unvisited_cells = set(maze.allCells())
        initial_cell = choice(list(unvisited_cells))
        unvisited_cells.remove(initial_cell)
        maze_set = {initial_cell}

        while unvisited_cells:
            current = choice(list(unvisited_cells))
            path = [current]

            while current not in maze_set:
                neighbors = maze.neighbours(current)
                valid_neighbors = [
                    neighbor
                    for neighbor in neighbors
                    if maze.checkCoordinates(neighbor)
                ]
                next_cell = choice(valid_neighbors)
                if next_cell in path:
                    path = path[: path.index(next_cell) + 1]
                else:
                    path.append(next_cell)
                current = next_cell

            for cell in path:
                maze_set.add(cell)
                unvisited_cells.discard(cell)

            for i in range(len(path) - 1):
                if maze.checkCoordinates(path[i]) and maze.checkCoordinates(
                    path[i + 1]
                ):
                    maze.removeWall(path[i], path[i + 1])

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

        self.m_mazeGenerated = True
