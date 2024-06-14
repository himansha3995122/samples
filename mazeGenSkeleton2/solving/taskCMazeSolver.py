from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D
from collections import deque


class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "taskC"

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.solveMazeTaskC(maze)

    def solveMazeTaskC(self, maze: Maze3D):
        self.m_solved = False
        # self.resetPathAndCellExplored()

        entrances = maze.getEntrances()
        exits = maze.getExits()

        print("Entrances: ", entrances)

        if not entrances or not exits:
            return

        closest_pair = None
        min_distance = float("inf")
        paths = {}

        for entrance in entrances:
            
            queue = deque([(entrance, 0)])
            visited = set()
            local_paths = {entrance: None}
            while queue:
                curr_cell, dist = queue.popleft()
                if curr_cell in exits:
                    if dist < min_distance:
                        min_distance = dist
                        closest_pair = (entrance, curr_cell)
                        paths = local_paths
                    break
                for neighbor in maze.neighbours(curr_cell):
                    if neighbor not in visited and not maze.hasWall(
                        curr_cell, neighbor
                    ):
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))  # type: ignore
                        local_paths[neighbor] = curr_cell  # type: ignore

        if closest_pair:
            entrance, exit = closest_pair
            self.solved(entrance, exit)
            self.tracePath(paths, exit)

    def tracePath(self, paths, exit):
        cell = exit
        while cell:
            self.solverPathAppend(cell, False)
            cell = paths[cell]
        self.solverPathAppend(cell, False)
