from pathlib import Path
from heapq import heappush, heappop


def parse(path):
    grid = {}
    with open(path) as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line.strip()):
                if char != "#":
                    grid[(i, j)] = char
    return grid


def solve(grid):
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    first_move = (0, 1)

    i, j = [pos for pos, char in grid.items() if char == "S"][0]
    end = [pos for pos, char in grid.items() if char == "E"][0]

    d = {(i, j, first_move): (0, set())}
    pq = [(0, i, j, first_move)]
    while pq:
        cost, i, j, last_move = heappop(pq)
        if cost > d[(i, j, last_move)][0]:
            continue

        for move in moves:
            if move == last_move:
                di, dj = move
                ni, nj = i + di, j + dj
                new_cost = cost + 1
                if (ni, nj) not in grid:
                    continue
            else:
                ni, nj = i, j
                new_cost = cost + 1000

            old_cost, prevs = d.get((ni, nj, move), (float("inf"), set()))
            if new_cost < old_cost:
                d[(ni, nj, move)] = (new_cost, {(i, j, last_move)})
                heappush(pq, (new_cost, ni, nj, move))
            elif new_cost == old_cost:
                prevs.add((i, j, last_move))

    part1 = float("inf")
    best_end = (*end, last_move)
    for move in moves:
        cost, prevs = d[(*end, move)]
        if cost < part1:
            part1 = cost
            best_end = (*end, move)

    visited = set()
    to_visit = [best_end]
    while to_visit:
        i, j, move = to_visit.pop()
        if (i, j, move) in visited:
            continue
        visited.add((i, j, move))
        for prev in d[(i, j, move)][1]:
            to_visit.append(prev)

    part2 = len(set((i, j) for i, j, move in visited))
    return part1, part2


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    grid = parse(path)
    print(solve(grid))


if __name__ == "__main__":
    main(example=False)
