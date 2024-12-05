from pathlib import Path
from collections import defaultdict


def is_valid(deps, update):
    for i in range(len(update) - 1):
        for j in range(i + 1, len(update)):
            if update[i] in deps[update[j]]:
                return False
    return True


def part1(deps, updates):
    result = 0
    for update in updates:
        if is_valid(deps, update):
            result += update[len(update) // 2]
    return result


def part2(deps, updates):
    result = 0
    for update in updates:
        if is_valid(deps, update):
            continue

        outgoing = defaultdict(list)
        in_count = defaultdict(int)
        for u in update:
            for v in update:
                if u == v:
                    continue
                if v in deps[u]:
                    outgoing[u].append(v)
                    in_count[v] += 1

        ready = []
        for page in update:
            if in_count[page] == 0:
                ready.append(page)

        order = []
        while ready:
            page = ready.pop()
            order.append(page)
            for v in outgoing[page]:
                in_count[v] -= 1
                if in_count[v] == 0:
                    ready.append(v)

        if len(order) != len(update):
            raise Exception("dependenies have cycle")

        result += order[len(order) // 2]

    return result


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    deps = defaultdict(set)
    updates = []
    with open(path) as f:
        first_half = True
        for line in f:
            if line == "\n":
                first_half = False
                continue

            if first_half:
                u, v = (int(x) for x in line.strip().split("|"))
                deps[u].add(v)
            else:
                updates.append([int(x) for x in line.strip().split(",")])

    print(part1(deps, updates))
    print(part2(deps, updates))


if __name__ == "__main__":
    main(example=False)
