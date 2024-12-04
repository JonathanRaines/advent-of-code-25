import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    """Find the sum of the differences between two sorted columns."""
    file: Path = parse_input()
    data: pd.DataFrame = pd.read_csv(file.as_posix(), sep=r"\s+", header=None)
    for col in data:
        data[col] = data[col].sort_values(ignore_index=True)
    data["distance"] = (data.iloc[:, 1] - data.iloc[:, 0]).abs()
    print(data.head())
    print(sum(data["distance"]))


def parse_input() -> str:
    """Accept user input."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str)
    args = parser.parse_args()
    return Path(args.input)


if __name__ == "__main__":
    main()
