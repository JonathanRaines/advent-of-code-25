import argparse
from dataclasses import dataclass
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import NamedTuple, Self

import numpy as np
from numpy.typing import NDArray

GUARD_SYMBOLS: str = "^>v<"


class State(StrEnum):
    FLOOR = "."
    OBSTACLE = "#"
    GUARD = "^"  # TODO directions


class Layer(IntEnum):
    MAP = 0
    TRAIL = 1


class Coordinate(NamedTuple):
    row: int
    col: int


class Direction(IntEnum):
    N = 0
    E = 1
    S = 2
    W = 3

    def next(self) -> Self:
        return Direction((self.value + 1) % 4)


@dataclass
class Guard:
    pos: Coordinate
    facing: Direction


@dataclass
class Env:
    obstacles: Coordinate
    guard: Guard
    trail: NDArray[np.bool]

    def step(self) -> bool:
        done = False
        self.trail[self.guard.pos] = True
        g_pos: Coordinate = self.guard.pos
        g_fac: Direction = self.guard.facing

        vertical = g_fac in [Direction.N, Direction.S]
        looking_neg = g_fac in [Direction.N, Direction.W]

        # Get the obstacles in the same row or column as the guard
        if vertical:
            inline = self.obstacles.row[self.obstacles.col == g_pos.col]
        else:
            inline = self.obstacles.col[self.obstacles.row == g_pos.row]

        # Get the guard pos in terms of the changing and static axis
        g_change = g_pos.row if vertical else g_pos.col
        g_static = g_pos.col if vertical else g_pos.row

        # Get the next obstacle in the direction the guard is facing
        if looking_neg:
            if inline[g_change > inline].size == 0:
                ahead = 0
                done = True
            else:
                ahead = np.max(inline[g_change > inline])
        if not looking_neg:
            if inline[g_change < inline].size == 0:
                ahead = self.trail.shape[0] if vertical else self.trail.shape[1]
                done = True
            else:
                ahead = np.min(inline[g_change < inline])

        next_inline = ahead + (1 if looking_neg else -1)
        g_new = (
            Coordinate(next_inline, g_static)
            if vertical
            else Coordinate(g_static, next_inline)
        )

        if vertical:
            slice = sorted([g_new.row, self.guard.pos.row])
            self.trail[
                slice[0] : slice[1],
                self.guard.pos.col,
            ] = True
        else:
            slice = sorted([self.guard.pos.col, g_new.col])
            self.trail[self.guard.pos.row, slice[0] : slice[1]] = True

        if done:
            self.guard = Guard(
                g_new,
                g_fac,
            )
            self.trail[g_new] = True
            return True

        self.guard = Guard(
            g_new,
            g_fac.next(),
        )

        return False

    def render(self) -> None:
        map = np.full_like(self.trail, State.FLOOR, dtype=str)
        map[self.obstacles] = State.OBSTACLE

        padded = np.pad(self.trail, (1, 1), mode="edge")

        map[self.trail] = "x"
        corner = (
            padded[2:, 1:-1].astype(int)
            + padded[:-2, 1:-1].astype(int)
            + padded[1:-1, 2:].astype(int)
            + padded[1:-1, :-2].astype(int)
            >= 2
        ).astype(bool)
        map[np.logical_and(corner, self.trail)] = "+"
        vertical = np.logical_and(padded[2:, :], padded[:-2, :])[:, 1:-1]
        map[np.logical_and(vertical, self.trail)] = "|"
        horizontal = np.logical_and(padded[:, 2:].astype(int), padded[:, :-2])[1:-1, :]
        map[np.logical_and(horizontal, self.trail)] = "-"

        guard_symbol = GUARD_SYMBOLS[self.guard.facing]
        map[self.guard.pos] = guard_symbol
        map_str = "\n".join(["".join(row) for row in map])
        print(map_str)


def main() -> None:
    grid_path = get_input()
    with grid_path.open("r") as file:
        grid_text = file.read()
    env: Env = parse_grid(grid_text)
    max_steps = 100
    for _ in range(max_steps):
        done = env.step()
        env.render()
        print("Walked: ", np.sum(env.trail))
        if done:
            print("Guard has left the grid")
            break


def get_input() -> Path:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "grid",
        type=str,
        help="Path to the grid file",
        default="day-6/test.txt",
        nargs="?",
    )
    args = parser.parse_args()
    return Path(args.grid)


def parse_grid(
    grid_text: str,
) -> Env:
    lines: list[str] = grid_text.splitlines()
    text_array = np.array([list(line) for line in lines])
    obstacles: tuple[NDArray] = np.where(text_array == State.OBSTACLE)
    guard: tuple[NDArray] = np.where(
        np.vectorize(lambda x: x in GUARD_SYMBOLS)(text_array),
    )
    direction: Direction = Direction(GUARD_SYMBOLS.index(text_array[guard][0]))

    return Env(
        obstacles=Coordinate(*obstacles),
        guard=Guard(
            Coordinate(guard[0][0], guard[1][0]),
            direction,
        ),
        trail=np.zeros_like(text_array, dtype=bool),
    )


if __name__ == "__main__":
    main()
