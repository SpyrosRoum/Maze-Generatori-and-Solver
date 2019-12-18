from PIL import Image
import numpy as np

import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Solver:
    def __init__(self, path):
        maze = Image.open(path)
        (self.width, self.height) = maze.size
        self.pixels = np.array(maze)

    def dead_end_filler(self, time_it=False):
        if time_it:
            start_time = time.time()

        for row, col in self.dead_ends_gen():
            self.pixels[row][col] = RED
            while (next_ := self.next_dead(row, col)) != (None, None):
                row, col = next_
                self.pixels[row][col] = RED

        if time_it:
            took = time.time() - start_time
            return Image.fromarray(self.pixels), took

        return Image.fromarray(self.pixels)

    def dead_ends_gen(self):
        for row in range(1, self.height-1):
            for col in range(1, self.width-1):
                if self.is_wall(row, col):
                    continue
                if self.is_dead_end(row, col):
                    yield (row, col)

    def next_dead(self, row, col):
        if row > 0 and self.is_white(row - 1, col):
            if self.is_dead_end(row - 1, col):
                return row - 1, col
        if row < self.height - 1 and self.is_white(row+1, col):
            if self.is_dead_end(row + 1, col):
                return row + 1, col
        if col > 0 and self.is_white(row, col-1):
            if self.is_dead_end(row, col - 1):
                return row, col - 1
        if col < self.width - 1 and self.is_white(row, col+1):
            if self.is_dead_end(row, col + 1):
                return row, col + 1

        return None, None

    def is_dead_end(self, row, col):
        if self.is_wall(row, col):
            return False
        up = 1
        down = 1
        left = 1
        right = 1
        if row > 0 and self.is_white(row-1, col):
            up = 0
        if row < self.height-1 and self.is_white(row+1, col):
            down = 0
        if col > 0 and self.is_white(row, col-1):
            left = 0
        if col < self.width-1 and self.is_white(row, col+1):
            right = 0

        return up + down + left + right == 3

    def is_wall(self, row, col):
        return self.pixels[row][col][1] == 0 # If it's white it will be 255

    def is_white(self, row, col):
        return self.pixels[row][col][1] == 255


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

