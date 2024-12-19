import argparse
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

import numpy as np
from numpy.typing import NDArray

PEAK_HEIGHT: int = 9
INDEX = "\033[90m"
CURRENT = "\033[47m"
FORK = "\033[44m"
MEET_UP = "\033[43m"
PATH = "\033[46m"
ENDC = "\033[0m"


Coord = tuple[int, int]


class Step(NamedTuple):
    """A step in a trail."""

    coord: Coord
    is_fork: bool  # Used only for visualisation
    is_meet_up: bool


Trail = list[Step]


def main() -> None:
    file, visualise = get_input()
    with file.open() as f:
        contents: str = f.read()

    # 0 low, 9 high
    topography: NDArray[np.int8] = parse_topography(contents)

    trailhead_coords: NDArray[np.intp] = np.argwhere(topography == 0)

    # Key; coord of trailhead, Value: dict peaks=set of peaks reachable from trailhead,
    # trails=set of trails
    trailheads: dict[Coord, dict[set[Coord], set[Trail]]] = {
        tuple(coord): {"peaks": set(), "trails": set()} for coord in trailhead_coords
    }

    # A meet up is the opposite of a fork, where two trails merge together.
    # Same format as trailheads
    meet_ups: dict[Coord, dict[set[Coord], set[Trail]]] = defaultdict(
        lambda: {"peaks": set(), "trails": set()},
    )

    for trailhead, trailhead_info in trailheads.items():
        # Initialise a queue of coordinates to explore
        coords_to_explore = [trailhead]

        # Keep track of the trail. Needed for updating meet_ups when reaching a peak.
        trail: Trail = []

        while coords_to_explore:
            coord: Coord = Coord(coords_to_explore.pop())

            height = topography[coord]

            # Height is a proxy for how far along the trail we are
            # Can use to trim the trail back to what it was at this coord
            if len(trail) > height:
                trail = trail[:height]
            if visualise:
                print_map(topography, trail, coord)

            # If we've been here before, we've already explored all options
            if coord in meet_ups:
                peaks_reachable: set[Coord] = meet_ups[coord]["peaks"]
                trail_ends: set[Trail] = meet_ups[coord]["trails"]
                trailhead_info["peaks"].update(peaks_reachable)

                # Need to backpropagate the trails from the meet_ups in the current trail.
                # Extend the trail ends from the meet up back to the start of the
                # current trail. Will then trim appropriately for each meet up.
                trails_from_trailhead = {
                    (*tuple(step.coord for step in trail), coord, *trail_end)
                    for trail_end in trail_ends
                }
                trailhead_info["trails"].update(trails_from_trailhead)
                meet_up_coords_in_trail = (
                    step.coord for step in trail if step.is_meet_up
                )
                for meet_up_coord in meet_up_coords_in_trail:
                    meet_ups[meet_up_coord]["peaks"].update(peaks_reachable)
                    trails_from_meet_up = {
                        tuple(
                            coord
                            for coord in _trail
                            if topography[coord] > topography[meet_up_coord]
                        )
                        for _trail in trails_from_trailhead
                    }
                    meet_ups[meet_up_coord]["trails"].update(trails_from_meet_up)
                continue

            # Reaching a peak
            if height == PEAK_HEIGHT:
                trail.append(
                    Step(
                        coord=coord,
                        is_meet_up=False,  # Doesn't matter anyway
                        is_fork=False,
                    ),
                )
                trailhead_info["peaks"].add(coord)
                trailhead_info["trails"].add(tuple(step.coord for step in trail))

                # Add this peak to all meet_ups along the trail
                meet_up_coords_in_trail = (
                    step.coord for step in trail if step.is_meet_up
                )
                for meet_up_coord in meet_up_coords_in_trail:
                    meet_ups[meet_up_coord]["peaks"].add(coord)
                    meet_ups[meet_up_coord]["trails"].add(
                        tuple(
                            step.coord
                            for step in trail
                            if topography[step.coord] > topography[meet_up_coord]
                        ),
                    )
                continue

            # Explore
            options = []
            inroads = 0
            # N E S W directions
            for delta in ((-1, 0), (0, 1), (1, 0), (0, -1)):
                neighbour = tuple(np.add(coord, delta))
                if not (
                    0 <= neighbour[0] < topography.shape[0]
                    and 0 <= neighbour[1] < topography.shape[1]
                ):
                    continue
                if topography[neighbour] == height - 1:
                    inroads += 1
                if topography[neighbour] == height + 1:
                    options.append(neighbour)

            # is_fork is used for visualisation
            # meet_ups (where trails merge together) are where we may rejoin from
            # another trail and so where we need to track.
            is_fork = len(options) > 1
            is_meet_up = inroads > 1

            trail.append(
                Step(
                    coord=coord,
                    is_meet_up=is_meet_up,
                    is_fork=is_fork,
                ),
            )

            coords_to_explore.extend(options)
    for trailhead, trailhead_info in trailheads.items():
        print(tuple(int(c) for c in trailhead), len(trailhead_info["trails"]))
    print(
        "Trails: ",
        sum(len(v["peaks"]) for v in trailheads.values()),
        "| Trail rating sum: ",
        sum(len(v["trails"]) for v in trailheads.values()),
    )


def get_input() -> tuple[Path, bool]:
    """Get the input file from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="The input file to read",
        type=str,
        nargs="?",
        default="day-10/test.txt",
    )
    parser.add_argument(
        "-v",
        "--visualise",
        help="Print the visualisation of the trail",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()
    return Path(args.input), args.visualise


def parse_topography(file_contents: str) -> NDArray[np.int8]:
    """Parse the file contents into a numpy array."""
    return np.array([list(row) for row in file_contents.splitlines()], dtype=np.int8)


def print_map(
    topography: NDArray[np.int8],
    trail: list[Step],
    coord: Coord,
) -> None:
    """Print the topography with the current location highlighted."""
    for _ in range(topography.shape[0] + 1):
        delete_line()

    forks = {step.coord for step in trail if step.is_fork}
    meet_ups = {step.coord for step in trail if step.is_meet_up}
    trail = {step.coord for step in trail}

    # Col indexes
    print("  ", end="")
    for i in range(topography.shape[0]):
        print(f"{INDEX} {i}{ENDC}", end="")
    print()
    for i_row, row in enumerate(topography):
        print(f"{INDEX} {i_row}{ENDC}", end="")
        for i_col, col in enumerate(row):
            if (i_row, i_col) == coord:
                print(f"{CURRENT} {col!s}{ENDC}", end="")
            elif (i_row, i_col) in forks:
                print(f"{MEET_UP} {col!s}{ENDC}", end="")
            elif (i_row, i_col) in meet_ups:
                print(f"{FORK} {col!s}{ENDC}", end="")
            elif (i_row, i_col) in trail:
                print(f"{PATH} {col!s}{ENDC}", end="")
            else:
                print(f" {col}", end="")
        print()


def delete_line():
    print("\033[1A\x1b[2K", end="")


if __name__ == "__main__":
    main()
