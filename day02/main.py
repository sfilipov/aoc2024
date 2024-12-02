from pathlib import Path


def is_safe(level):
    inc, dec = False, False
    for a, b in zip(level, level[1:]):
        if abs(a - b) == 0 or abs(a - b) > 3:
            return False
        if a > b:
            dec = True
        else:
            inc = True
    return not (inc and dec)


def part1(levels):
    return sum(1 for level in levels if is_safe(level))


def part2(levels):
    safe = 0
    for level in levels:
        if is_safe(level):
            safe += 1
        elif any(is_safe(level[:i] + level[i + 1 :]) for i in range(len(level))):
            safe += 1
    return safe


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    with open(path) as f:
        lines = f.readlines()

    levels = []
    for line in lines:
        level = [int(num) for num in line.strip().split()]
        levels.append(level)

    print(part1(levels))
    print(part2(levels))


if __name__ == "__main__":
    main()
