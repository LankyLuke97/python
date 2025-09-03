from collections import defaultdict
from datetime import datetime
import heapq
import math
from pathlib import Path
import png
import random

IMG_WIDTH, IMG_HEIGHT = 800, 800

# Colour presets
RED    = [255,   0,   0]
GREEN  = [  0, 255,   0]
BLUE   = [  0,  0,  255]
YELLOW = [255, 255,   0]

lower, upper = 30, 100
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

    # Image settings
    scale = min(IMG_HEIGHT // m, IMG_WIDTH // n)
    timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
    Path(timestamp).mkdir()
    image = create_base_image(grid, scale)
    image_count = 0

    w = png.Writer(width=n*scale, height=m*scale, bitdepth=8, greyscale=False)

    with open(f'{timestamp}/frame_{image_count:05}.png', "wb") as f:
        w.write(f, image)
    prev = start

    while open_set:
        image_count += 1
        update_image(image, prev[0], prev[1], scale, RED) 
        current_f_score, current_y, current_x = heapq.heappop(open_set)
        current = (current_y, current_x)
        update_image(image, current[0], current[1], scale, BLUE)
        if current == goal: 
            path = reconstruct_path(back_pointers, goal)
            break
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
        prev = current

        with open(f'{timestamp}/frame_{image_count:05}.png', "wb") as f:
            w.write(f, image)

    if not path:
        print("NO PATH FOUND")
        return
    
    for y, x in path[:-1]:
        image_count += 1
        update_image(image, y, x, scale, GREEN)

        with open(f'{timestamp}/frame_{image_count:05}.png', "wb") as f:
            w.write(f, image)
    update_image(image, path[-1][0], path[-1][1], scale, YELLOW)
    with open(f'{timestamp}/frame_{image_count+1:05}.png', "wb") as f:
        w.write(f, image)

def create_base_image(grid, scale):
    min_val = min(map(min, grid))
    max_val = max(map(max, grid))
    normalise = 255 / max_val - min_val
    
    image = []
    for row in grid:
        image_row = []
        for v in row:
            v *= normalise
            image_row.extend([int(v)] * 3 * scale)
        image.extend([image_row] * scale)
    return image

def update_image(image, y, x, scale, new_colour):
    y *= scale
    x *= scale * 3
    replace_row = new_colour * scale
    for i in range(scale):
        image[y+i][x:x+len(replace_row)] = replace_row

search(start, dest, grid, m, n)
