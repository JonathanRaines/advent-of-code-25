import argparse
from collections import defaultdict
from pathlib import Path


def main() -> None:
    input_file = get_input()
    with Path(input_file).open("r") as file:
        text = file.read()

    rules, print_orders = separate_rules_and_print_orders(text)
    forward_rules, backward_rules = parse_rules(rules)
    print_orders = parse_print_orders(print_orders)

    middle_page_number_total: int = 0
    bad_orders = []
    for page_order in print_orders:
        if not order_is_ok(page_order, forward_rules, backward_rules):
            bad_orders.append(page_order)
            continue
        middle_page_number_total += get_middle_page_number(page_order)

    print(middle_page_number_total)


def get_input() -> str:
    """Get the input file from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The input file to read")
    args = parser.parse_args()
    return args.input


def separate_rules_and_print_orders(lines: str) -> tuple[list[str], list[str]]:
    """Split input file on empty line."""
    rules_text, print_orders_text = lines.split("\n\n")
    return rules_text.splitlines(), print_orders_text.splitlines()


def parse_rules(rules: list[str]) -> tuple[dict[int, set[int]], dict[int, set[int]]]:
    """Convert list of strings to forward and backward lookups.

    ["47|53", "47|13", "97|13"] -> {47: {53, 13}, 97: {13}}, {53: {47}, 13: {47, 97}}
    """
    strings = [rule.split("|") for rule in rules]
    int_tuples = [(int(rule[0]), int(rule[1])) for rule in strings]
    forward = defaultdict(set)
    backward = defaultdict(set)
    for before, after in int_tuples:
        forward[before].add(after)
        backward[after].add(before)

    return forward, backward


def parse_print_orders(print_orders: list[str]) -> list[list[int]]:
    """Convert list of strings to list of lists of integers.

    [["75, 47,..., 23"], ...] -> [[75, 47,..., 23], ...]
    """
    print_orders = [order.split(",") for order in print_orders]
    return [[int(page) for page in orders] for orders in print_orders]


def order_is_ok(
    order: list[int],
    forward_rules: dict[int, set[int]],
    backward_rules=dict[int, set[int]],
) -> bool:
    """Check if the order is valid."""
    # Step through each page number in the order.
    for index, page in enumerate(order):
        # Check no overlap between backwards rules and the order after the current page.
        if len(backward_rules.get(page, set()).intersection(order[index + 1 :])) > 0:
            return False
        # Check no overlap between forward rules and the order before the current page.
        if len(forward_rules.get(page, set()).intersection(order[:index])) > 0:
            return False
    return True


def get_middle_page_number(order: list[int]) -> int:
    """Return the middle page number in the order."""
    return order[len(order) // 2]


if __name__ == "__main__":
    main()
