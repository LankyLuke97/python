from collections import defaultdict
from datetime import datetime
import heapq
import math
from pathlib import Path
import png
import random

lower, upper = 5, 10
m, n = random.randint(lower,upper), random.randint(lower,upper)
density = random.randint(5,20)
directions = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

grid = [[0 if random.randint(0, 100) > density else 1 for _ in range(n)] for _ in range(m)]
grid[0][0] = 0
grid[m-1][n-1] = 0
start = (0, 0)
dest = (m-1, n-1)

def reconstruct_path(back_pointers, current):
    total_path = [current]
    while current in back_pointers:
        current = back_pointers[current]
        total_path.append(current)
    return total_path[::-1]

def search(start, goal, grid, m, n):
    start_y, start_x = start

    open_set = [(0, start_y, start_x)]
    back_pointers = {}

    g_score = defaultdict(lambda: math.inf)
    g_score[(start_y, start_x)] = 0

    while open_set:
        current_f_score, current_y, current_x = heapq.heappop(open_set)
        current = (current_y, current_x)
        if current == goal: return reconstruct_path(back_pointers, goal)
        for dy, dx in directions:
            y, x = current_y + dy, current_x + dx
            if y < 0 or y >= m or x < 0 or x >= n or grid[y][x] == 1: continue
            neighbour = (y, x)
            tentative_g_score = g_score[current] + grid[y][x]
            
            if tentative_g_score < g_score[neighbour]:
                back_pointers[neighbour] = current
                g_score[neighbour] = tentative_g_score
                f_score = tentative_g_score + abs(goal[0] - y) + abs(goal[1] - x)
                heapq.heappush(open_set, (f_score, y, x))

    return []

def create_image(grid):
    image = []
    for row in grid:
        image_row = []
        for v in row:
            image_row.extend(v)
        image.append(image_row)
    return image

def visualise(grid, path):
    min_val = min(map(min, grid))
    max_val = max(map(max, grid))
    normalise = 255 / max_val - min_val

    grid = [[[int((v - min_val) * normalise), int((v - min_val) * normalise), int((v - min_val) * normalise)] for v in row] for row in grid]
    timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
    image = create_image(grid)
    Path(timestamp).mkdir()
    frame_len = math.ceil(math.log(len(path)+1,10))

    w = png.Writer(width=n, height=m, bitdepth=8, greyscale=False)

    with open(f'{timestamp}/frame_{0:0>{frame_len}}.png', "wb") as f:
        w.write(f, image)

    for i in range(len(path)):
        y, x = path[i]
        grid[y][x] = [255, 0, 0]
        image = create_image(grid)

        with open(f'{timestamp}/frame_{(i+1):0>{frame_len}}.png', "wb") as f:
            w.write(f, image)

path = search(start, dest, grid, m, n)
visualise(grid, path)
