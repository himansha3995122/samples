from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
from random import choice


class TaskDMazeGenerator(MazeGenerator):
    """
    Task D maze generator.
    """

    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        startLevel = 0
        startCoord = Coordinates3D(startLevel, 0, 0)

        visited = set([startCoord])
        stack = [startCoord]

        while stack:
            currCell = stack.pop()
            neighbours = maze.neighbours(currCell)
            nonVisitedNeighs = [
                neigh
                for neigh in neighbours
                if neigh not in visited
                and (
                    neigh.getRow() >= 0
                    and neigh.getRow() < maze.rowNum(neigh.getLevel())
                )
                and (
                    neigh.getCol() >= 0
                    and neigh.getCol() < maze.colNum(neigh.getLevel())
                )
            ]

            if nonVisitedNeighs:
                stack.append(currCell)
                neighbour = choice(nonVisitedNeighs)
                maze.removeWall(currCell, neighbour)
                visited.add(neighbour)
                stack.append(neighbour)

        self.m_mazeGenerated = True
