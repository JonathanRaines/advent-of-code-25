import argparse
from dataclasses import dataclass
from pathlib import Path

from tqdm import tqdm


@dataclass(frozen=True)
class Equation:
    result: int
    atoms: tuple[int]


@dataclass(frozen=True)
class Node:
    atoms_remaining: tuple[int]
    current_value: int


def main() -> None:
    input_path: Path = get_input()
    with input_path.open("r") as f:
        equations = f.read().splitlines()

    total_of_correct: int = 0
    for equation_str in tqdm(equations):
        equation: Equation = parse_equation(equation_str)
        queue: list[Node] = [Node(equation.atoms[1:], equation.atoms[0])]

        while queue:
            node: Node = queue.pop()
            if not node.atoms_remaining:
                if node.current_value == equation.result:
                    total_of_correct += equation.result
                    break
                continue
            children: list[Node] = [
                Node(
                    node.atoms_remaining[1:],
                    func(node.current_value, node.atoms_remaining[0]),
                )
                for func in [add, mul, concat]
            ]
            # Operations only increase the value
            queue.extend(
                [child for child in children if child.current_value <= equation.result],
            )

    print("total_of_correct: ", total_of_correct)


def get_input() -> Path:
    """Get the input file from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input",
        help="The input file to read",
        type=str,
        nargs="?",
        default="day-7/test.txt",
    )
    args = parser.parse_args()
    return Path(args.input)


def parse_equation(equation: str) -> Equation:
    parts: list[str] = equation.split(" ")
    answer: str = int(parts[0].removesuffix(":"))
    atoms: tuple[str] = tuple(int(a) for a in parts[1:])
    return Equation(answer, atoms)


def add(a: int, b: int) -> int:
    return a + b


def mul(a: int, b: int) -> int:
    return a * b


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


if __name__ == "__main__":
    main()
