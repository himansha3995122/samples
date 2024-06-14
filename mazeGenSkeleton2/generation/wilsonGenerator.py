# wilsonGenerator.py
# -------------------------------------------------------------------
# Wilson's algorithm maze generator.
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
from random import choice, shuffle


class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson's algorithm maze generator.
    """

    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        unvisited = set(maze.allCells())
        start_cell = choice(list(unvisited))
        unvisited.remove(start_cell)
        in_maze = {start_cell}

        while unvisited:
            current_cell = choice(list(unvisited))
            path = [current_cell]

            while current_cell not in in_maze:
                neighbors = maze.neighbours(current_cell)
                valid_neighbors = [n for n in neighbors if maze.checkCoordinates(n)]
                next_cell = choice(valid_neighbors)
                if next_cell in path:
                    path = path[: path.index(next_cell) + 1]
                else:
                    path.append(next_cell)
                current_cell = next_cell

            for cell in path:
                in_maze.add(cell)
                unvisited.discard(cell)

            for i in range(len(path) - 1):
                if maze.checkCoordinates(path[i]) and maze.checkCoordinates(
                    path[i + 1]
                ):
                    maze.removeWall(path[i], path[i + 1])

        # Ensure outer walls are kept intact
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
