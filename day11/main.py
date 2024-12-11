from pathlib import Path
from collections import Counter


def calc(stones, steps):
    freq = Counter(stones)
    for _ in range(steps):
        freq = step(freq)
    return sum(freq.values())


def step(freq):
    new_freq = Counter()
    for stone, count in freq.items():
        s = str(stone)
        if stone == 0:
            new_freq[1] += count
        elif len(s) % 2 == 0:
            a, b = int(s[: len(s) // 2]), int(s[len(s) // 2 :])
            new_freq[a] += count
            new_freq[b] += count
        else:
            new_freq[stone * 2024] += count
    return new_freq


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    with open(path) as f:
        line = f.readline().strip()

    stones = [int(num) for num in line.split()]
    print(calc(stones, 25))
    print(calc(stones, 75))


if __name__ == "__main__":
    main(example=False)
