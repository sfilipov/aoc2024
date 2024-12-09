from pathlib import Path
from collections import defaultdict


def solve(grid):
    char_grid = defaultdict(list)
    for pos, char in grid.items():
        if char != ".":
            char_grid[char].append(pos)

    part1 = set()
    for vals in char_grid.values():
        for idx1 in range(1, len(vals)):
            for idx2 in range(idx1):
                a, b = vals[idx1], vals[idx2]
                diff = b - a
                p1 = a - diff
                p2 = b + diff
                part1.update(p for p in (p1, p2) if p in grid)

    part2 = set()
    for vals in char_grid.values():
        for idx1 in range(1, len(vals)):
            for idx2 in range(idx1):
                a, b = vals[idx1], vals[idx2]
                diff = b - a
                cur = a
                while cur in grid:
                    part2.add(cur)
                    cur -= diff
                cur = b
                while cur in grid:
                    part2.add(cur)
                    cur += diff

    return (len(part1), len(part2))


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    with open(path) as f:
        grid = {}
        for j, line in enumerate(f):
            for i, char in enumerate(list(line.strip())):
                grid[complex(i, j)] = char

    print(solve(grid))


if __name__ == "__main__":
    main(example=False)
