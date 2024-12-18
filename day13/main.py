from pathlib import Path


def parse(path):
    def parse_button(line):
        button, xy = line.split(": ")
        x, y = xy.split(", ")
        x, x_move = x.split("+")
        y, y_move = y.split("+")
        return (int(x_move), int(y_move))

    def parse_prize(line):
        prize, xy = line.split(": ")
        x, y = xy.split(", ")
        x, x_move = x.split("=")
        y, y_move = y.split("=")
        return (int(x_move), int(y_move))

    with open(path) as f:
        lines = [line.strip() for line in f]

    problems = []
    for i in range(0, len(lines), 4):
        a = parse_button(lines[i])
        b = parse_button(lines[i + 1])
        prize = parse_prize(lines[i + 2])
        problems.append((a, b, prize))

    return problems


def solve_problem(problem):
    button_a, button_b, targets = problem
    ax, ay = button_a
    bx, by = button_b
    target_x, target_y = targets

    # ax * A + bx * B = target_x
    # ay * A + by * B = target_y

    a_factor = ay / ax
    new_by = by - a_factor * bx
    new_target_y = target_y - a_factor * target_x
    B = new_target_y / new_by
    A = (target_x - bx * B) / ax
    A, B = round(A, 2), round(B, 2)

    if A.is_integer() and B.is_integer():
        return 3 * int(A) + int(B)
    else:
        return 0


def solve(problems):
    part1 = 0
    for problem in problems:
        part1 += solve_problem(problem)

    add = 10000000000000
    part2 = 0
    for problem in problems:
        problem = (problem[0], problem[1], (problem[2][0] + add, problem[2][1] + add))
        part2 += solve_problem(problem)

    return (part1, part2)


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")
    problems = parse(path)
    print(solve(problems))


if __name__ == "__main__":
    main(example=False)
