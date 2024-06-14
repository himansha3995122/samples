from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from collections import deque


class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation (Alternative Version).
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"

    def solveMazeTaskC(self, maze: Maze3D):
        self.m_solved = False
        self.resetPathAndCellExplored()

        entrances = maze.getEntrances()
        exits = maze.getExits()

        if not entrances or not exits:
            return

        optimal_pair = None
        minimum_distance = float("inf")
        path_map = {}

        for entry in entrances:
            search_queue = deque([(entry, 0)])
            seen_cells = set()
            local_paths = {entry: None}
            while search_queue:
                current_cell, distance = search_queue.popleft()
                if current_cell in exits:
                    if distance < minimum_distance:
                        minimum_distance = distance
                        optimal_pair = (entry, current_cell)
                        path_map = local_paths
                    break
                for neighbor in maze.neighbours(current_cell):
                    if neighbor not in seen_cells and not maze.hasWall(
                        current_cell, neighbor
                    ):
                        seen_cells.add(neighbor)
                        search_queue.append((neighbor, distance + 1))  # type: ignore
                        local_paths[neighbor] = current_cell  # type: ignore

        if optimal_pair:
            entry, exit = optimal_pair
            self.solved(entry, exit)
            self.buildPath(path_map, exit)

    def buildPath(self, paths, exit):
        current = exit
        while current:
            self.solverPathAppend(current, False)
            current = paths[current]
        self.solverPathAppend(current, False)
