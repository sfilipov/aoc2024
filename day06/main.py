from pathlib import Path


DIR_MAP = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0),
}


def find_start(grid):
    m, n = len(grid), len(grid[0])
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "^":
                return (i, j)


def gen_jump(grid):
    m, n = len(grid), len(grid[0])
    jump = {}
    for i in range(m):
        cur_dir = (0, -1)
        nxt_dir = DIR_MAP[cur_dir]
        end = (i, -1, nxt_dir)
        for j in range(n):
            if grid[i][j] != "#":
                jump[(i, j, cur_dir)] = end
            else:
                end = (i, j + 1, nxt_dir)

        cur_dir = (0, 1)
        nxt_dir = DIR_MAP[cur_dir]
        end = (i, n, nxt_dir)
        for j in range(n - 1, -1, -1):
            if grid[i][j] != "#":
                jump[(i, j, cur_dir)] = end
            else:
                end = (i, j - 1, nxt_dir)

    for j in range(n):
        cur_dir = (-1, 0)
        nxt_dir = DIR_MAP[cur_dir]
        end = (-1, j, nxt_dir)
        for i in range(m):
            if grid[i][j] != "#":
                jump[(i, j, cur_dir)] = end
            else:
                end = (i + 1, j, nxt_dir)

        cur_dir = (1, 0)
        nxt_dir = DIR_MAP[cur_dir]
        end = (m, j, nxt_dir)
        for i in range(m - 1, -1, -1):
            if grid[i][j] != "#":
                jump[(i, j, cur_dir)] = end
            else:
                end = (i - 1, j, nxt_dir)

    return jump


def get_visited(grid, jump, start, obstacle=None):
    def in_grid(grid, i, j):
        return 0 <= i < len(grid) and 0 <= j < len(grid[0])

    m, n = len(grid), len(grid[0])
    cur_dir = (-1, 0)

    visited = set()
    i, j = start
    while in_grid(grid, i, j) and (i, j, cur_dir) not in visited:
        visited.add((i, j, cur_dir))
        if not obstacle or obstacle[0] == i or obstacle[1] == j:
            di, dj = cur_dir
            ni, nj = i + di, j + dj

            if in_grid(grid, ni, nj) and (grid[ni][nj] == "#" or (ni, nj) == obstacle):
                cur_dir = DIR_MAP[cur_dir]
            else:
                i, j = ni, nj
        else:
            i, j, cur_dir = jump[(i, j, cur_dir)]

    return (set((i, j) for i, j, cur_dir in visited), (i, j, cur_dir) in visited)


def count_obstacles(grid, visited, jump, start):
    m, n = len(grid), len(grid[0])
    loops = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "." and (i, j) in visited:
                v, has_loop = get_visited(grid, jump, start, (i, j))
                if has_loop:
                    loops += 1
    return loops


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    with open(path) as f:
        grid = [list(line.strip()) for line in f]

    m, n = len(grid), len(grid[0])
    jump = gen_jump(grid)
    start = find_start(grid)
    visited, _ = get_visited(grid, jump, start)
    part1 = len(visited)
    part2 = count_obstacles(grid, visited, jump, start)
    print(part1, part2)


if __name__ == "__main__":
    main(example=False)
