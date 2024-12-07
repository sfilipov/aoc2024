from pathlib import Path


def backtrack(target, nums, concat):
    if len(nums) == 1:
        return nums[0] == target

    a, b = nums[0], nums[1]
    return any(
        [
            backtrack(target, [a + b] + nums[2:], concat),
            backtrack(target, [a * b] + nums[2:], concat),
            concat and backtrack(target, [int(str(a) + str(b))] + nums[2:], concat),
        ]
    )


def calc(eqs, concat):
    result = 0
    for target, nums in eqs:
        if backtrack(target, nums, concat):
            result += target
    return result


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    eqs = []
    with open(path) as f:
        for line in f:
            result, nums = line.strip().split(": ")
            eqs.append((int(result), [int(num) for num in nums.split()]))

    print(calc(eqs, concat=False))
    print(calc(eqs, concat=True))


if __name__ == "__main__":
    main(example=False)
