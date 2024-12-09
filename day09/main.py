from pathlib import Path


def part1(disk_map):
    n = sum(disk_map)
    blocks = [None] * n
    files = []
    spaces = []
    is_disk = True
    file_id = 0
    i = 0
    for size in disk_map:
        if is_disk:
            for _ in range(size):
                files.append((i, file_id))
                blocks[i] = file_id
                i += 1
            file_id += 1
        else:
            for _ in range(size):
                spaces.append(i)
                i += 1
        is_disk = not is_disk

    spaces.reverse()
    while spaces and files and spaces[-1] < files[-1][0]:
        space = spaces.pop()
        i, file_id = files.pop()
        blocks[space] = file_id
        blocks[i] = None

    result = 0
    i = 0
    while i < n and blocks[i] is not None:
        result += i * blocks[i]
        i += 1

    return result


def part2(disk_map):
    n = sum(disk_map)
    blocks = [None] * n
    files = []
    spaces = []
    is_disk = True
    file_id = 0
    i = 0
    for size in disk_map:
        if is_disk:
            files.append((i, i + size, file_id))
            blocks[i : i + size] = [file_id] * size
            file_id += 1
        else:
            spaces.append((i, i + size))

        i += size
        is_disk = not is_disk

    spaces.reverse()

    for file_start, file_end, file_id in reversed(files):
        space = None
        for j in range(len(spaces) - 1, -1, -1):
            space_start, space_end = spaces[j]
            if space_end - space_start >= file_end - file_start:
                space = j
                break

        if space is None:
            continue
        if space_start > file_start:
            continue

        space_start, space_end = spaces[j]
        file_size = file_end - file_start
        space_size = space_end - space_start
        blocks[space_start : space_start + file_size] = [file_id] * file_size
        blocks[file_start:file_end] = [None] * file_size
        if space_size == file_size:
            spaces.pop(j)
        else:
            new_space_start = space_start + file_size
            spaces[j] = (new_space_start, space_end)

    result = 0
    i = 0
    while i < n:
        if blocks[i] is not None:
            result += i * blocks[i]
        i += 1

    return result


def main(example=False):
    main_path = Path(__file__)
    path = main_path.with_name("input_example.txt" if example else "input.txt")

    with open(path) as f:
        disk_map = [int(x) for x in f.readline().strip()]

    print(part1(disk_map))
    print(part2(disk_map))


if __name__ == "__main__":
    main(example=False)
