import re
from pathlib import Path


def main() -> None:
    with Path("day-3/input.txt").open("r") as file:
        instructions = file.read().splitlines()

    instructions = "do()" + "".join(instructions)

    # Match do() and don't() instructions, up to the next do() or don't().
    # Capture the do() or don't() conditional, and the instructions
    conditionals = re.findall(
        r"(do(?>n't)?\(\))(.*?)(?=do(?>n't)?\(\)|$)",
        instructions,
    )

    # Get the instructions for do() instructions.
    to_do = [
        instructions for condition, instructions in conditionals if condition == "do()"
    ]

    matches = re.findall(r"mul\(([0-9]*),([0-9]*)\)", "".join(to_do))

    answer = sum([int(a) * int(b) for a, b in matches])
    print(answer)  # 81135289 too low, 97363801 too high


if __name__ == "__main__":
    main()
