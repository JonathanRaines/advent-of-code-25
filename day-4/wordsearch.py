import argparse
import re
from pathlib import Path

SEARCH: str = "XMAS"
ANY: str = r"(?>.|\n)"  # Non capturing group that matches any character across newlines


def main() -> None:
    search_word, grid_path = get_input()
    with Path(grid_path).open("r") as f:
        grid = f.read()

    width: int = len(grid.splitlines()[0])
    patterns: list[str] = make_pattern(search_word, width)

    n_matchs: list[int] = [len(re.findall(p, grid)) for p in patterns]
    print("Matches:", sum(n_matchs))


def get_input() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str, help="Word to search for")
    parser.add_argument("grid", type=str, help="Path to word search grid .txt file")
    args = parser.parse_args()
    return args.word, args.grid


def make_pattern(word: str, grid_size: int) -> str:
    patterns: list[str] = [
        # Horizontal forward and backward
        word,
        word[::-1],
        # Major diagonal down and up
        f"{ANY}{{{grid_size-1}}}".join(word),
        f"{ANY}{{{grid_size-1}}}".join(word[::-1]),
        # Vertical down and up
        f"{ANY}{{{grid_size}}}".join(word),
        f"{ANY}{{{grid_size}}}".join(word[::-1]),
        # Minor diagonal down and up
        f"{ANY}{{{grid_size+1}}}".join(word),
        f"{ANY}{{{grid_size+1}}}".join(word[::-1]),
    ]

    # Wrap each pattern in capturing group inside a forward lookahead to allow mating of
    # overlapping patterns
    overlapping_patterns: list[str] = [f"(?=({pattern}))" for pattern in patterns]

    # Join with OR
    return overlapping_patterns


if __name__ == "__main__":
    main()
