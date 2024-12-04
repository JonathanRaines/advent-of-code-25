from pathlib import Path

MAX_SAFE_CHANGE: int = 3
MIN_SAFE_CHANGE: int = 1


def main() -> None:
    """Count safe readings."""
    with Path("day-2/input.txt").open("r") as f:
        readings = f.read().splitlines()

    safe: int = 0
    for reading in readings:
        levels: list[int] = [int(x) for x in reading.split()]

        if is_safe(levels):
            safe += 1
    print("Safe: ", safe)


def is_safe(reading: list[int]) -> bool:
    """Check if a reading is safe."""
    # Get the deltas between each value
    diff: list[int] = [
        x1 - x2 for x1, x2 in zip(reading[1:], reading[:-1], strict=True)
    ]

    # Care about the absolute size of diffs for comparing step sizes.
    abs_diff: list[int] = [abs(d) for d in diff]

    if max(abs_diff) > MAX_SAFE_CHANGE:
        return False
    if min(abs_diff) < MIN_SAFE_CHANGE:
        return False
    return all(delta > 0 for delta in diff) or all(delta < 0 for delta in diff)


if __name__ == "__main__":
    main()
