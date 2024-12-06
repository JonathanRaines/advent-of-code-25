import argparse
import re
from pathlib import Path

SEARCH: str = "XMAS"
ANY: str = r"(?>.|\n)"  # Non capturing group that matches any character across newlines


def main() -> None:
    """Find Xs of an input word."""
    search_word, grid_path = get_input()
    with Path(grid_path).open("r") as f:
        grid = f.read()

    width: int = len(grid.splitlines()[0])
    pattern: str = make_pattern(search_word, width)
    print(pattern)

    n_matchs: int = len(re.findall(pattern, grid))
    print("Matches:", n_matchs)  # 1679 too low.


def get_input() -> tuple[str, str]:
    """Get input from command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("word", type=str, help="Word to search for")
    parser.add_argument("grid", type=str, help="Path to word search grid .txt file")
    args = parser.parse_args()
    return args.word, args.grid


def make_pattern(word: str, grid_size: int) -> str:
    """Create a regex pattern to match an X the input word in a grid."""
    patterns: list[str] = [
        # Minor diagonal down and up
        f"{ANY}{{{grid_size-1}}}".join(word),
        f"{ANY}{{{grid_size-1}}}".join(word[::-1]),
        # Major diagonal down and up
        f"{ANY}{{{grid_size+1}}}".join(word),
        f"{ANY}{{{grid_size+1}}}".join(word[::-1]),
    ]

    # Wrap each pattern in capturing group inside a forward lookahead to allow mating of
    # overlapping patterns
    overlapping_patterns: list[str] = [f"(?=({pattern}))" for pattern in patterns]
    min_u, min_d, maj_u, maj_d = overlapping_patterns

    # Find a major diagonal in either direction, followed by two characters, followed by
    # a minor. The two characters are the start of the major diagonal (*) (as it's
    # non-consuming) and the intermediate (^).
    # *M ^.  S
    #  .  A  .
    #  M  .  S
    return f"(?=({maj_u}|{maj_d}).{{2}}({min_u}|{min_d}))"


if __name__ == "__main__":
    main()
