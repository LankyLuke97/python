from collections import defaultdict
import heapq
import math
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

def search(start, goal):
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

path = search(start, dest)
for row in grid:
    print(row)
print('------------------------------------')

if not path: print("Did not find path")
else:
    for loc in path:
        print(loc)


