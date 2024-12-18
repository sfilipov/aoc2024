from pathlib import Path


class Node:
    def __init__(self, size, val):
        self.parent = self
        self.size = size
        self.val = val

    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent

    def union(self, other):
        a, b = self.find(), other.find()
        if a == b:
            return
        b.parent = a
        a.size += b.size


def parse(path):
    robots = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            pstr, vstr = line.split()
            _, pxy = pstr.split("=")
            px, py = map(int, pxy.split(","))
            _, vxy = vstr.split("=")
            vx, vy = map(int, vxy.split(","))
            robots.append((px, py, vx, vy))
    return robots


def count_robots(robots, w, h):
    counts = [[0] * w for _ in range(h)]
    for robot in robots:
        counts[robot[1]][robot[0]] += 1
    return counts


def print_counts(counts):
    for row in counts:
        chars = [str(count) if count > 0 else "." for count in row]
        print("".join(chars))


def move_robots(robots, w, h, moves):
    for i in range(len(robots)):
        px, py, vx, vy = robots[i]
        px = (px + moves * vx) % w
        py = (py + moves * vy) % h
        robots[i] = px, py, vx, vy


def partition_sizes(counts):
    moves = [
        (i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == 0 and j == 0)
    ]

    nodes = {}
    for y, row in enumerate(counts):
        for x, count in enumerate(row):
            if count > 0:
                nodes[(x, y)] = Node(count, (x, y))

    stack = list(nodes)
    visited = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if (nx, ny) in nodes and (nx, ny) not in visited:
                stack.append((nx, ny))
                nodes[(x, y)].union(nodes[(nx, ny)])

    sizes = set()
    for node in nodes.values():
        sizes.add(node.size)

    return sizes


def part1(robots, w, h):
    move_robots(robots, w, h, 100)
    a = b = c = d = 0
    mid_w, mid_h = w // 2, h // 2
    for px, py, _, _ in robots:
        if px < mid_w and py < mid_h:
            a += 1
        elif px > mid_w and py < mid_h:
            b += 1
        elif px < mid_w and py > mid_h:
            c += 1
        elif px > mid_w and py > mid_h:
            d += 1

    return a * b * c * d


def part2(robots, w, h):
    move_count = 0
    while True:
        move_count += 1
        move_robots(robots, w, h, 1)
        counts = count_robots(robots, w, h)
        sizes = partition_sizes(counts)
        if max(sizes) > 50:
            return move_count


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    robots = parse(path)
    w, h = (11, 7) if example else (101, 103)
    print(part1(list(robots), w, h))
    print(part2(list(robots), w, h))


if __name__ == "__main__":
    main(example=False)
