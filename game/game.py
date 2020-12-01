import numpy as np
from threading import Thread, Timer
from game.random import random_move
from game.exception import GridSizeNotValidException, MoveException, NoEmptyTileException, NoTileFoundException


MIN_SIZE = 2
MAX_SIZE = 10
DEFAULT_SIZE = 3


def build_grid(size=DEFAULT_SIZE):
    if not MIN_SIZE <= size <= MAX_SIZE:
        raise GridSizeNotValidException
    grid = np.arange(size ** 2).tolist()
    grid.append(grid.pop(0))
    print(np.array(grid).reshape(size, size))
    return np.array(grid).reshape(size, size)

def build_grid_test(size=DEFAULT_SIZE):
    grid=[[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    return np.array(grid).reshape(size, size)

def find_tile(grid, value):
    y = 0
    while y < 3:
        x = 0
        while x < 3:
            if int(grid[y][x]) == int(value):
                return [y, x]
            x += 1
        y += 1
    raise NoTileFoundException('The grid does not contain this tile')


def find_empty_tile(grid):
    try:
        return find_tile(grid, 0)
    except NoTileFoundException:
        raise NoEmptyTileException


def movable_tiles(grid):
    length = 3
    y, x = find_empty_tile(grid)

    tiles = []
    if y - 1 >= 0:
        tiles.append(grid[y - 1][x])
    if x + 1 < length:
        tiles.append(grid[y][x + 1])
    if y + 1 < length:
        tiles.append(grid[y + 1][x])
    if x - 1 >= 0:
        tiles.append(grid[y][x - 1])

    return list(map(int, tiles))


def move(grid, tile_to_move_arg):
    tile_to_move = int(tile_to_move_arg)

    if tile_to_move not in movable_tiles(grid):
        raise MoveException('This tile cannot be moved')

    try:
        empty_y, empty_x = find_empty_tile(grid)
        new_y, new_x = find_tile(grid, tile_to_move)
    except NoEmptyTileException:
        raise MoveException('There is not empty tile to move this tile')
    except NoTileFoundException:
        raise MoveException('This tile does not exist')

    new_grid = grid.copy()
    new_grid[empty_y][empty_x] = grid[new_y][new_x]
    new_grid[new_y][new_x] = grid[empty_y][empty_x]
    return new_grid

def move_letter(grid, action):

    try:
        empty_y, empty_x = find_empty_tile(grid)
        new_y=empty_y
        new_x=empty_x
    except NoEmptyTileException:
        raise MoveException('There is not empty tile to move this tile')
    
    if action.lower() == "l":
        if empty_x == 0:
            raise MoveException("You can't move that way!")
        else:
            new_x=empty_x-1
    elif action.lower() == "r":
        if empty_x == 2:
            raise MoveException("You can't move that way!")
        else:
            new_x=empty_x+1
    elif action.lower() == "u":
        if empty_y == 0:
            raise MoveException("You can't move that way!")
        else:
            new_y=empty_y-1
    elif action.lower() == "d":
        if empty_y == 2:
            raise MoveException("You can't move that way!")
        else:
            new_y=empty_y+1
    else:
        raise MoveException("direction does not exist! (L/R/U/D)")
    
    new_grid = grid.copy()
    new_grid[empty_y][empty_x] = grid[new_y][new_x]
    new_grid[new_y][new_x] = grid[empty_y][empty_x]
    return new_grid


def is_grid_resolved(grid, started_grid):
    return np.array_equal(grid, started_grid)


class ShuffleThread(Thread):
    def __init__(self, grid):
        Thread.__init__(self)
        self.grid = grid
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            self.grid = move(self.grid, random_move(movable_tiles(self.grid)))

    def stop(self):
        self.running = False

    def result(self):
        test = find_empty_tile(self.grid)
        x = self.grid[1][1]
        self.grid[1][1] = 0
        self.grid[test[0]][test[1]] = x
        return self.grid


def shuffle(grid, timeout=1):
    shuffle_thread = ShuffleThread(grid.copy())
    time_thread = Timer(timeout, shuffle_thread.stop)

    shuffle_thread.start()
    time_thread.start()

    shuffle_thread.join()

    return shuffle_thread.result()
