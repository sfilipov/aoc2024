from pathlib import Path


def parse(path):
    with open(path) as f:
        lines = [line.strip() for line in f]

    idx = lines.index("")
    grid_lines = lines[:idx]
    moves = "".join(lines[idx + 1 :])

    grid = {}
    for y, row in enumerate(grid_lines):
        for x, char in enumerate(row):
            grid[complex(x, y)] = char

    return grid, moves


def widen_grid(grid):
    new_grid = {}
    new_chars = {
        ".": "..",
        "#": "##",
        "O": "[]",
        "@": "@.",
    }
    for pos, char in grid.items():
        a, b = new_chars[char]
        new_grid[complex(2 * pos.real, pos.imag)] = a
        new_grid[complex(2 * pos.real + 1, pos.imag)] = b

    return new_grid


def get_move(move):
    move_map = {
        "<": -1 + 0j,
        ">": 1 + 0j,
        "^": 0 - 1j,
        "v": 0 + 1j,
    }
    return move_map[move]


def part1(grid, moves):
    def find_free(grid, pos, move):
        cur = pos
        while grid[cur] == "O":
            cur += get_move(move)
        return cur if grid[cur] == "." else None

    start = [pos for pos, char in grid.items() if char == "@"][0]
    cur = start
    for move in moves:
        nxt = cur + get_move(move)
        if grid[nxt] == ".":
            grid[cur] = "."
            grid[nxt] = "@"
            cur = nxt
        elif grid[nxt] == "O":
            free = find_free(grid, nxt, move)
            if free:
                grid[free] = "O"
                grid[cur] = "."
                grid[nxt] = "@"
                cur = nxt

    result = 0
    for pos, char in grid.items():
        if char == "O":
            result += 100 * pos.imag + pos.real
    return int(result)


def part2(grid, moves):
    def find_free_hor(grid, pos, move):
        cur = pos
        while grid[cur] in "[]":
            cur += get_move(move)
        return cur if grid[cur] == "." else None

    def try_move(grid, pos, move):
        if grid[pos] == ".":
            return True
        if grid[pos] == "#":
            return False

        stack = [pos]
        if grid[pos] == "[":
            stack.append(pos + 1)
        else:
            stack.append(pos - 1)

        visit_order = []
        while stack:
            pos = stack.pop()
            visit_order.append(pos)
            nxt = pos + get_move(move)
            if grid[nxt] == "#":
                return False
            elif grid[nxt] == ".":
                visit_order.append(nxt)
            elif grid[nxt] == "[":
                stack.append(nxt)
                stack.append(nxt + 1)
            else:
                stack.append(nxt)
                stack.append(nxt - 1)

        visited = set()
        for pos in reversed(visit_order):
            if pos in visited:
                continue
            visited.add(pos)
            if grid[pos] == ".":
                continue
            grid[pos + get_move(move)] = grid[pos]
            grid[pos] = "."

        return True

    start = [pos for pos, char in grid.items() if char == "@"][0]
    cur = start
    for i, move in enumerate(moves):
        nxt = cur + get_move(move)
        if grid[nxt] == ".":
            grid[cur] = "."
            grid[nxt] = "@"
            cur = nxt
        elif grid[nxt] in "[]":
            if move in "<>":
                opp_move = "<" if move == ">" else ">"
                free = find_free_hor(grid, nxt, move)
                if not free:
                    continue
                while free != cur:
                    grid[free] = grid[free + get_move(opp_move)]
                    free += get_move(opp_move)
                grid[cur] = "."
                cur = nxt
            else:
                success = try_move(grid, nxt, move)
                if success:
                    grid[nxt] = "@"
                    grid[cur] = "."
                    cur = nxt

    result = 0
    for pos, char in grid.items():
        if char == "[":
            result += 100 * pos.imag + pos.real
    return int(result)


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    grid, moves = parse(path)
    wide_grid = widen_grid(grid)
    print(part1(grid, moves))
    print(part2(wide_grid, moves))


if __name__ == "__main__":
    main(example=False)
