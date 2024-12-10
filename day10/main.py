from pathlib import Path


def solve(grid, unique):
    moves = (0 + 1j, 0 - 1j, 1 + 0j, -1 + 0j)
    result = 0
    for pos, val in grid.items():
        if val != 0:
            continue

        stack = [pos]
        visited = set()
        while stack:
            node = stack.pop()
            if unique:
                if node in visited:
                    continue
                visited.add(node)
            if grid[node] == 9:
                result += 1
            for move in moves:
                if node + move in grid and grid[node + move] == grid[node] + 1:
                    stack.append(node + move)

    return result


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    with open(path) as f:
        grid = {}
        for y, line in enumerate(f):
            for x, digit in enumerate(line.strip()):
                grid[complex(x, y)] = int(digit)

    print(solve(grid, unique=True))
    print(solve(grid, unique=False))


if __name__ == "__main__":
    main(example=False)
