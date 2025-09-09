import argparse
from collections import defaultdict
from datetime import datetime
import heapq
import glob
import math
from pathlib import Path
from PIL import Image
import png
import random
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--width', default="800")
parser.add_argument('--height', default="800")
parser.add_argument('-l', '--lower', default="10")
parser.add_argument('-u', '--upper', default="50")
parser.add_argument('-v', '--visualise', action='store_true')

args = parser.parse_args()

IMG_WIDTH, IMG_HEIGHT = int(args.width), int(args.height)

# Colour presets
RED    = [255,   0,   0]
GREEN  = [  0, 255,   0]
BLUE   = [  0,  0,  255]
YELLOW = [255, 255,   0]

lower, upper = int(args.lower), int(args.upper)
m, n = random.randint(lower,upper), random.randint(lower,upper)
directions = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]

grid = [[random.randint(1, 100) for _ in range(n)] for _ in range(m)]
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

    g_score = {}
    g_score[(start_y, start_x)] = 0

    if args.visualise:
        # Image settings
        scale = min(IMG_HEIGHT // m, IMG_WIDTH // n)
        timestamp = datetime.now().strftime('%y%m%d_%H%M%S')
        Path(timestamp).mkdir()
        
        base_image = create_base_image(grid, scale)
        image = [row.copy() for row in base_image]
        image_count = 0

        w = png.Writer(width=n*scale, height=m*scale, bitdepth=8, greyscale=False)

        with open(f'{timestamp}/frame_{image_count:05}.png', "wb") as f:
            w.write(f, image)
    prev = start

    while open_set:
        current_f_score, current_y, current_x = heapq.heappop(open_set)
        current = (current_y, current_x)
        if args.visualise:
            update_image(image, prev[0], prev[1], scale, RED) 
            update_image(image, current[0], current[1], scale, BLUE)
        if current == goal: 
            path = reconstruct_path(back_pointers, goal)
            break
        for dy, dx in directions:
            y, x = current_y + dy, current_x + dx
            neighbour = (y, x)
            if neighbour in g_score or y < 0 or y >= m or x < 0 or x >= n or grid[y][x] == 1: continue
            _g_score = g_score[current] + grid[y][x]
            back_pointers[neighbour] = current
            g_score[neighbour] = _g_score
            f_score = _g_score + abs(goal[0]-y) + abs(goal[1] - x)
            heapq.heappush(open_set, (f_score, y, x))
        if args.visualise:
            prev = current
            image_count += 1
            with open(f'{timestamp}/frame_{image_count:05}.png', "wb") as f:
                w.write(f, image)

    if not path:
        print("NO PATH FOUND")
        return
    if not args.visualise: return
    
    for y, x in path[:-1]:
        image_count += 1
        update_image(base_image, y, x, scale, GREEN)
        with open(f'{timestamp}/frame_{image_count:05}.png', "wb") as f:
            w.write(f, base_image)
    update_image(base_image, path[-1][0], path[-1][1], scale, YELLOW)
    with open(f'{timestamp}/frame_{image_count+1:05}.png', "wb") as f:
        w.write(f, base_image)
    combine_images(timestamp)
    clean_up(timestamp)

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

def combine_images(folder):
    images = []
   
    files = glob.glob(f"{folder}/*.png")
    if len(files) < 1000:
        for filename in sorted(files):
            images.append(Image.open(filename))

        images.extend([images[-1]]*15)
        duration = len(images) // 30
        images[0].save(f"{folder}.gif", save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
    else:
        subprocess.run(["ffmpeg","-r","60","-i",f"{folder}/frame_%05d.png","-vcodec","libx264","-crf","25",f"{folder}.mp4"])

def clean_up(folder):
    for root, dirs, files in Path(folder).walk(top_down=False):
        for name in files:
            (root / name).unlink()
        for name in dirs:
            (root / name).rmdir()
    Path(folder).rmdir()
search(start, dest, grid, m, n)
