from pathlib import Path
from collections import Counter


def part1(left, right):
    result = 0
    for a, b in zip(left, right):
        result += abs(a - b)
    return result


def part2(left, right):
    counter = Counter(right)
    result = 0
    for num in left:
        result += num * counter[num]
    return result


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    with open(path) as f:
        lines = f.readlines()
    left, right = [], []
    for line in lines:
        a, b = map(int, line.strip().split())
        left.append(a)
        right.append(b)

    left.sort()
    right.sort()

    print(part1(left, right))
    print(part2(left, right))


if __name__ == "__main__":
    main()
