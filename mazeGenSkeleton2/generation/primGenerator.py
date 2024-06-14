# primGenerator.py
# -------------------------------------------------------------------
# Prim's maze generator.
# -------------------------------------------------------------------

from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
from random import choice, shuffle


class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.
    """

    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        # Start with a random cell
        start_cell = Coordinates3D(0, 0, 0)
        cells_in_maze = {start_cell}
        walls = [
            (start_cell, neighbor)
            for neighbor in maze.neighbours(start_cell)
            if maze.checkCoordinates(neighbor)
        ]

        while walls:
            wall = choice(walls)
            cell1, cell2 = wall

            if cell2 not in cells_in_maze:
                cells_in_maze.add(cell2)
                maze.removeWall(cell1, cell2)
                for neighbor in maze.neighbours(cell2):
                    if neighbor not in cells_in_maze and maze.checkCoordinates(
                        neighbor
                    ):
                        walls.append((cell2, neighbor))

            walls.remove(wall)

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
