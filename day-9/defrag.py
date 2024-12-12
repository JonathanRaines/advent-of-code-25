import argparse
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def main() -> None:
    input: Path = get_input()
    with input.open() as f:
        disk_map: str = f.read().replace("\n", "")
    disk: NDArray[np.int16] = expand_disk_map(disk_map)

    lead_pointer: int = len(disk) - 1
    trail_pointer: int = 0

    while lead_pointer < len(disk):
        # Stop if meeting in the middle.
        if trail_pointer == lead_pointer:
            break
        # If the trail pointer is in a file, move it right.
        if disk[trail_pointer] >= 0:
            trail_pointer += 1
            continue
        # If the lead pointer is in a gap, move it left.
        if disk[lead_pointer] < 0:
            lead_pointer -= 1
            continue
        # If reached here, trail is in a gap and lead is in a file.
        # swap the two.
        disk[trail_pointer] = disk[lead_pointer]
        disk[lead_pointer] = -1

    cs: int = checksum(disk)
    print(cs)


def get_input() -> Path:
    """Get the input file from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="The input file to read",
        type=str,
        nargs="?",
        default="day-9/test.txt",
    )
    args = parser.parse_args()
    return Path(args.input)


def expand_disk_map(disk_map: str) -> NDArray:
    """Expand the disk map into a 1D array of disk blocks."""
    file_sizes: list[int] = [int(x) for x in disk_map[::2]]
    gap_sizes: list[int] = [int(x) for x in disk_map[1::2]]
    files: list[int] = [[i] * size for i, size in enumerate(file_sizes)]
    gaps: list[int] = [[-1] * size for size in gap_sizes]
    disk_blocks: list[list[int]] = [
        x for pair in zip(files[:-1], gaps, strict=True) for x in pair
    ]
    disk_blocks.append(files[-1])

    return np.concatenate(disk_blocks).astype(np.int16)


def checksum(disk: NDArray) -> int:
    """Calculate the checksum of the disk.

    It's the sum of the product of the position and the file size for each file.
    """
    files = disk[disk >= 0]
    positions = np.arange(len(files))
    return np.sum(files * positions)


if __name__ == "__main__":
    main()
