import argparse
import random
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
BLUE   = [  0,  0,  255]
YELLOW = [255, 255,   0]

density = float(args.density)
number_of_points = int(args.number)

def create_points(num_points):
    return [(random.randrange(0,IMG_WIDTH), random.randrange(0,IMG_HEIGHT)) for _ in range(num_points)]

def spanning_tree(graph):
    pass

print(create_points(number_of_points))
