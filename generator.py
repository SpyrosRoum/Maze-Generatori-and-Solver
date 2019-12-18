import random
from queue import LifoQueue
from collections import namedtuple

import numpy as np
from PIL import Image


def generate_maze(width, height):
    Cell = namedtuple('cell', ['row', 'col'])

    maze = Image.new('RGB', (width*2+1, height*2+1), 0)

    pixels = maze.load()
    cells = np.zeros((width, height), dtype=int)

    first = Cell(random.randint(0, width-1), 0)
    cells[first.row][first.col] = 1

    pixels[cell_to_img(first)] = (255, 255, 255)
    pixels[first.row * 2 + 1, 0] = (255, 255, 255)
    pixels[-2, -1] = (255, 255, 255)

    stack = LifoQueue()
    stack.put(first)

    while not stack.empty():
        current = stack.get()
        row = current.row
        col = current.col

        adjacent = []
        if col < height - 1 and cells[row, col + 1] == 0:
            adjacent.append(Cell(row, col + 1))
        if col > 0 and cells[row, col - 1] == 0:
            adjacent.append(Cell(row, col - 1))
        if row > 0 and cells[row - 1, col] == 0:
            adjacent.append(Cell(row - 1, col))
        if row < width - 1 and cells[row + 1, col] == 0:
            adjacent.append(Cell(row + 1, col))

        if adjacent != []:
            next_cell = random.choice(adjacent)
            stack.put(current)

            # remove wall
            pixels[next_cell.row + row + 1, next_cell.col + col + 1] = (255, 255, 255)

            pixels[cell_to_img(current)] = (255, 255, 255)
            pixels[cell_to_img(next_cell)] = (255, 255, 255)

            cells[next_cell.row][next_cell.col] = 1

            stack.put(next_cell)


    return maze


def cell_to_img(cell):
    return cell.row * 2 + 1, cell.col * 2 + 1

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("width", nargs="?", type=int, default=32)
    parser.add_argument("height", nargs="?", type=int, default=None)
    parser.add_argument('--output', '-o', nargs='?', type=str, default='generated_maze.png')
    args = parser.parse_args()

    size = (args.width, args.height) if args.height else (args.width, args.width)

    maze = generate_maze(*size)
    maze.save(args.output)


