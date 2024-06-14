from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator
from random import choice


class TaskDMazeGenerator(MazeGenerator):
    """
    Task D maze generator (Alternative Version).
    """

    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        initial_level = 0
        initial_coord = Coordinates3D(initial_level, 0, 0)

        visited_cells = {initial_coord}
        cell_stack = [initial_coord]

        while cell_stack:
            current_cell = cell_stack.pop()
            neighbors = maze.neighbours(current_cell)
            unvisited_neighbors = [
                neighbor
                for neighbor in neighbors
                if neighbor not in visited_cells
                and 0 <= neighbor.getRow() < maze.rowNum(neighbor.getLevel())
                and 0 <= neighbor.getCol() < maze.colNum(neighbor.getLevel())
            ]

            if unvisited_neighbors:
                cell_stack.append(current_cell)
                chosen_neighbor = choice(unvisited_neighbors)
                maze.removeWall(current_cell, chosen_neighbor)
                visited_cells.add(chosen_neighbor)
                cell_stack.append(chosen_neighbor)

        self.m_mazeGenerated = True
