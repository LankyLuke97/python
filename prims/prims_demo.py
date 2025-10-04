from array import array
import argparse
from datetime import datetime
import random
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--width', default="800")
parser.add_argument('--height', default="800")
parser.add_argument('-d', '--density', default=0.5)
parser.add_argument('-n', '--number', default=100)
parser.add_argument('-v', '--visualise', action='store_true')

args = parser.parse_args()

if args.visualise:
    from pathlib import Path
    from PIL import Image
    import png

IMG_WIDTH, IMG_HEIGHT = int(args.width), int(args.height)

# Colour presets
RED    = [255,   0,   0]
GREEN  = [  0, 255,   0]
BLUE   = [  0,   0, 255]
YELLOW = [255, 255,   0]

density = float(args.density)
number_of_points = int(args.number)
timestamp = datetime.now().strftime('%y%m%d_%H%M%S')

def create_points(num_points):
    return [(random.randrange(0,IMG_WIDTH), random.randrange(0,IMG_HEIGHT)) for _ in range(num_points)]

def draw_bresenham_circle(x_centre, y_centre, r, image):
    width, height = len(image[0]) // 3, len(image)
    def mirror_eight(x, y):
        for i, j in [( x,  y), ( y,  x), (-x,  y), (-y,  x), ( x, -y), ( y, -x), (-x, -y), (-y, -x)]:
            i += x_centre
            j += y_centre
            if i < 0 or i >= width or j < 0 or j >= height: continue
            image[j][i*3:i*3+3] = [0, 0, 0]

    x, y = 0, -r
    f_m = 1-r
    d_e = 3
    d_ne = -(r<<1) + 5
    mirror_eight(x, y)

    while x < -y:
        if f_m <= 0: f_m += d_e
        else:
            f_m += d_ne
            d_ne += 2
            y += 1
        d_e += 2
        d_ne += 2
        x += 1
        mirror_eight(x, y)

def spanning_tree(graph):
    pass

points = create_points(number_of_points)
image = [[255] * 3 * IMG_WIDTH for _ in range(IMG_HEIGHT)]

for x, y in points:
    image[y][x*3:x*3+3] = [0,0,0]
    draw_bresenham_circle(x, y, 5, image)

w = png.Writer(width=IMG_WIDTH, height=IMG_HEIGHT, bitdepth=8, greyscale=False)

Path(timestamp).mkdir()
with open(f'{timestamp}/frame_00000.png', 'wb') as f:
    w.write(f, image)
