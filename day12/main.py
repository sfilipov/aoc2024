from pathlib import Path
from collections import defaultdict


class Node:
    def __init__(self, val):
        self.parent = self
        self.size = 1
        self.val = val

    def find(self):
        if self.parent != self:
            self.parent = self.parent.find()
        return self.parent

    def union(self, other):
        a, b = self.find(), other.find()
        if a == b:
            return
        less = min(a, b, key=lambda node: node.size)
        more = max(b, a, key=lambda node: node.size)
        less.parent = more
        more.size += less.size


def partition_groups(grid):
    nodes = {pos: Node(pos) for pos in grid}
    visited = set()
    moves = [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]
    for pos in grid:
        stack = [pos]
        while stack:
            pos = stack.pop()
            if pos in visited:
                continue
            visited.add(pos)
            for move in moves:
                if (
                    pos + move in grid
                    and pos + move not in visited
                    and grid[pos] == grid[pos + move]
                ):
                    nodes[pos].union(nodes[pos + move])
                    stack.append(pos + move)
    partitions = defaultdict(set)
    for pos, node in nodes.items():
        partitions[node.find().val].add(pos)

    return partitions


def normalise(a, b):
    if a == b:
        raise Exception
    x = min(a, b, key=lambda p: (p.real, p.imag))
    y = max(a, b, key=lambda p: (p.real, p.imag))
    return x, y


def build_fence(grid, partition):
    moves = {
        1 + 0j: (0.5 + 0.5j, 0.5 - 0.5j),
        -1 + 0j: (-0.5 + 0.5j, -0.5 - 0.5j),
        0 + 1j: (0.5 + 0.5j, -0.5 + 0.5j),
        0 - 1j: (0.5 - 0.5j, -0.5 - 0.5j),
    }
    all_segments = set()
    segments = defaultdict(list)
    for pos in partition:
        for move in moves:
            if pos + move in partition:
                continue
            di, dj = moves[move]
            i, j = pos + di, pos + dj
            segments[i].append(j)
            segments[j].append(i)
            all_segments.add(normalise(i, j))

    paths = []
    while segments:
        i = list(segments)[0]
        j = segments[i].pop()
        segments[j].remove(i)

        path = []
        while True:
            path.append(i)

            if not segments[j]:
                break

            i, j = j, segments[j].pop()
            segments[j].remove(i)

        start = min(path, key=lambda point: (point.real, point.imag))
        idx = path.index(start)
        path = path[idx:] + path[:idx] + [path[idx]]
        paths.append(path)

        for k, v in list(segments.items()):
            if len(v) == 0:
                del segments[k]

    lines = []
    for path in paths:
        line = [path[0]]
        for i in range(1, len(path) - 1):
            a, b, c = line[-1], path[i], path[i + 1]
            in_line = a.real == b.real == c.real or a.imag == b.imag == c.imag
            all_dir = all(normalise(b + move, b) in all_segments for move in moves)
            if in_line and not all_dir:
                continue
            line.append(b)

        lines.append(line)

    return (paths, lines)


def calc(grid):
    partitions = partition_groups(grid)

    part1_result = 0
    part2_result = 0
    for partition in partitions.values():
        area = len(partition)
        paths, lines = build_fence(grid, partition)
        perimeter = sum(len(points) - 1 for points in paths)
        faces = sum(len(points) for points in lines)
        part1_result += area * perimeter
        part2_result += area * faces

    return (part1_result, part2_result)


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    with open(path) as f:
        grid = {
            complex(x, y): char
            for y, line in enumerate(f)
            for x, char in enumerate(line.strip())
        }

    print(calc(grid))


if __name__ == "__main__":
    main(example=False)
