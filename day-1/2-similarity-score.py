import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    """Find the sum of the differences between two sorted columns."""
    file: Path = parse_input()
    data: pd.DataFrame = pd.read_csv(file.as_posix(), sep=r"\s+", header=None)
    data.columns = ["left", "right"]

    counts: pd.Series = data["right"].value_counts()

    similarity = data["left"].to_frame().join(counts, how="left", on="left")
    similarity["score"] = similarity["left"] * similarity["count"]

    score: float = similarity["score"].sum()

    print("Score: ", score)


def parse_input() -> str:
    """Accept user input."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    args = parser.parse_args()
    return Path(args.input)


if __name__ == "__main__":
    main()
