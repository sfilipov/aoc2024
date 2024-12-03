from pathlib import Path


def tokenizer(s: str):
    n = len(s)
    tokens = []
    i = 0
    while i < n:
        if s[i : i + 4] == "mul(":
            tokens.append("mul(")
            i += 4
        elif s[i : i + 4] == "do()":
            tokens.append("do()")
            i += 4
        elif s[i : i + 7] == "don't()":
            tokens.append("don't()")
            i += 7
        elif s[i].isdigit():
            end = i
            while end < n and s[end].isdigit():
                end += 1
            tokens.append(s[i:end])
            i = end
        else:
            tokens.append(s[i])
            i += 1
    return tokens


def sum_tokens(lines, force_enabled):
    result = 0
    enabled = True
    for line in lines:
        tokens = tokenizer(line)
        i = 0
        while i < len(tokens):
            if tokens[i] == "do()":
                enabled = True
                i += 1
            elif tokens[i] == "don't()":
                enabled = False
                i += 1
            elif (
                i + 4 < len(tokens)
                and tokens[i] == "mul("
                and tokens[i + 1].isdigit()
                and tokens[i + 2] == ","
                and tokens[i + 3].isdigit()
                and tokens[i + 4] == ")"
            ):
                if enabled or force_enabled:
                    result += int(tokens[i + 1]) * int(tokens[i + 3])
                i += 5
            else:
                i += 1
    return result


def part1(lines):
    return sum_tokens(lines, True)


def part2(lines):
    return sum_tokens(lines, False)


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    with open(path) as f:
        lines = [line.strip() for line in f.readlines()]

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
