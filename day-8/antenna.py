import argparse
import itertools
from pathlib import Path

import numpy as np
from numpy.typing import NDArray


def main() -> None:
    input: Path = get_input()
    with input.open() as f:
        data: str = f.read()

    shape = (len(data.splitlines()), len(data.splitlines()[0]))

    # Freq: Locations. Locations are NDArrays of shape (N, 2) [[x1, y1], [x2, y2], ...]
    antennae_locations: dict[str, NDArray] = parse_antenna_layout(data)

    node_coords = []
    for char, coords in antennae_locations.items():
        antenna_pairs = list(itertools.combinations(range(len(coords)), 2))
        deltas = [coords[pair[1]] - coords[pair[0]] for pair in antenna_pairs]
        minor_node_coords = [
            coords[pair[0]] - deltas[i] for i, pair in enumerate(antenna_pairs)
        ]
        major_node_coords = [
            coords[pair[1]] + deltas[i] for i, pair in enumerate(antenna_pairs)
        ]
        node_coords.extend(minor_node_coords + major_node_coords)

    node_array = np.array(node_coords)
    in_range_nodes = node_array[
        np.where(
            np.logical_and(
                (node_array >= 0).all(axis=1),
                (node_array < shape).all(axis=1),
            ),
        )
    ]
    unique_in_range_nodes = np.unique(in_range_nodes, axis=0)

    print(render_antennae_and_nodes(antennae_locations, unique_in_range_nodes, shape))
    print(len(unique_in_range_nodes))  # 321 too low.


def get_input() -> Path:
    """Get the input file from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="The input file to read",
        type=str,
        nargs="?",
        default="day-8/test.txt",
    )
    args = parser.parse_args()
    return Path(args.input)


def parse_antenna_layout(input: str) -> NDArray:
    """Parse the antenna layout from the input file."""
    unique_chars: set[str] = set(input).difference([".", "\n"])
    grid: NDArray = np.array([list(row) for row in input.splitlines()])

    return {char: np.array(np.where(grid == char)).T for char in unique_chars}


def render_antennae_and_nodes(
    antennae: dict[str, NDArray],
    nodes,
    size: tuple[int, int],
) -> None:
    """Render the antenna layout and nodes."""
    grid = np.full(size, ".", dtype=str)

    for node in nodes:
        grid[tuple(node)] = "#"

    for char, coords in antennae.items():
        for coord in coords:
            grid[tuple(coord)] = char

    return "\n".join(["".join(row) for row in grid])


if __name__ == "__main__":
    main()
