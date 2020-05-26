from PIL import Image
import numpy as np

import time

from dead_end_filler import DeadEndFiller



class Solver:
    def __init__(self, path):
        maze = Image.open(path)
        (self.width, self.height) = maze.size
        self.pixels = np.array(maze)

    def dead_end_filler(self, time_it=False):
        return DeadEndFiller(self.width, self.height, self.pixels).solve(time_it=time_it)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("maze", nargs="?", type=str, default=None)
    parser.add_argument('--output', '-o', nargs='?', type=str, default='solved.png')
    args = parser.parse_args()


    solver = Solver(args.maze)
    maze = solver.dead_end_filler()
    maze.save(args.output)

    # import timeit
    # solver = Solver('mazes/1920_1080.png')
    # t = timeit.timeit(solver.solve, number=1)
    # print(t)
    # solved = solver.solve()
    # solved.show()

