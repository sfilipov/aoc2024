from pathlib import Path


def part1(grid):
    m, n = len(grid), len(grid[0])
    count = 0
    for i in range(m):
        for j in range(n):
            count += count_xmas(grid, i, j)
    return count


def count_xmas(grid, i, j):
    if grid[i][j] != "X":
        return 0

    m, n = len(grid), len(grid[0])
    dirs = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0]

    count = 0
    for di, dj in dirs:
        if 0 <= i + 3 * di < m and 0 <= j + 3 * dj < n:
            word = [grid[i + k * di][j + k * dj] for k in range(1, 4)]
            if "".join(word) == "MAS":
                count += 1
    return count


def part2(grid):
    m, n = len(grid), len(grid[0])
    count = 0
    for i in range(m):
        for j in range(n):
            if is_mas(grid, i, j):
                count += 1
    return count


def is_mas(grid, i, j):
    m, n = len(grid), len(grid[0])
    if grid[i][j] != "A":
        return False
    if i == 0 or i == m - 1 or j == 0 or j == n - 1:
        return False
    a = grid[i - 1][j - 1]
    b = grid[i - 1][j + 1]
    c = grid[i + 1][j - 1]
    d = grid[i + 1][j + 1]
    return set([a, d]) == set([b, c]) == set("MS")


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    with open(path) as f:
        grid = [list(line.strip()) for line in f]

    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
