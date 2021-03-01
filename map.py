from settings import *
import random


def get_start(l, w):
    if random.choice([True, False]):
        if random.choice([True, False]):
            s = (0, random.randint(0, w - 1))
        else:
            s = (l - 1, random.randint(0, w - 1))
    else:
        if random.choice([True, False]):
            s = (random.randint(0, l - 1), 0)
        else:
            s = (random.randint(0, l - 1), w - 1)
    return s


def step_choice(x, y, r_matrix):
    step_list = []
    if x > 0:
        if not r_matrix[x - 1][y]:
            step_list.append((x - 1, y))
    if x < len(r_matrix) - 1:
        if not r_matrix[x + 1][y]:
            step_list.append((x + 1, y))
    if y > 0:
        if not r_matrix[x][y - 1]:
            step_list.append((x, y - 1))
    if y < len(r_matrix[0]) - 1:
        if not r_matrix[x][y + 1]:
            step_list.append((x, y + 1))
    if step_list:
        nx, ny = random.choice(step_list)
        if x == nx:
            if ny > y:
                tx, ty = x * 2, ny * 2 - 1
            else:
                tx, ty = x * 2, ny * 2 + 1
        else:
            if nx > x:
                tx, ty = nx * 2 - 1, y * 2
            else:
                tx, ty = nx * 2 + 1, y * 2
        return nx, ny, tx, ty
    else:
        return -1, -1, -1, -1


def generate_map(l, w):
    reach_matrix = []
    for i in range(l):  # создаём матрицу достижимости ячеек
        reach_matrix.append([])
        for j in range(w):
            reach_matrix[i].append(False)
    transition_matrix = []
    for i in range(l * 2 - 1):  # заполнение матрицы переходов
        transition_matrix.append([])
        for j in range(w * 2 - 1):
            if i % 2 == 0 and j % 2 == 0:
                transition_matrix[i].append(True)
            else:
                transition_matrix[i].append(False)
    entry = get_start(l, w)
    list_transition = [entry]
    x, y = entry
    reach_matrix[x][y] = True
    x, y, tx, ty = step_choice(x, y, reach_matrix)
    for i in range(1, w * l):
        while not (x >= 0 and y >= 0):
            x, y = list_transition[-1]
            list_transition.pop()
            x, y, tx, ty = step_choice(x, y, reach_matrix)
        reach_matrix[x][y] = True
        list_transition.append((x, y))
        transition_matrix[tx][ty] = True
        x, y, tx, ty = step_choice(x, y, reach_matrix)
    res = ["1" * (len(transition_matrix[1]) + 2)]
    for elem in transition_matrix:
        row = ["1"]
        for dot in elem:
            if dot:
                row.append(".")
            else:
                row.append("1")
        row.append("1")
        res.append("".join(row))
    res.append("1" * (len(transition_matrix[1]) + 2))
    for elem in res:
        print(elem)
    return res


text_map = generate_map(6, 6)
world_map = {}
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == '1':
                world_map[(i * TILE, j * TILE)] = '1'