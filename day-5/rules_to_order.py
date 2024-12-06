import argparse
from collections.abc import Iterable
from pathlib import Path

import networkx as nx


def main() -> None:
    input_file = get_input()
    with Path(input_file).open("r") as file:
        text = file.read()

    rule_strings, page_orders_strings = separate_rules_and_page_orders(text)
    rules = parse_rules(rule_strings)
    # The rules are actually cyclical so aren't universally applicable. This is evil.
    # Some must not apply to make the challenge possible.
    # Only rules where both numbers are present in an order are applicable.
    page_orders = parse_print_orders(page_orders_strings)
    applicable_rules = [
        filter_applicable_rules(rules, [order]) for order in page_orders
    ]
    allowed_page_orders: tuple[int] = [
        order_from_rules(rules) for rules in applicable_rules
    ]

    good_orders = [
        order
        for order, allowed in zip(page_orders, allowed_page_orders, strict=False)
        if order_is_ok(order, allowed)
    ]
    middle_pages = [get_middle_page_number(order) for order in good_orders]
    print("Sum of good order middle pages: ", sum(middle_pages))
    bad_orders = set(page_orders) - set(good_orders)
    bad_allowed_orders = [
        allowed_page_orders[page_orders.index(order)] for order in bad_orders
    ]

    corrected_orders = correct_order(bad_orders, bad_allowed_orders)

    corrected_middle_pages = [
        get_middle_page_number(order) for order in corrected_orders
    ]
    print("Sum of corrected order middle pages: ", sum(corrected_middle_pages))


def get_input() -> str:
    """Get the input file from the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="The input file to read")
    args = parser.parse_args()
    return args.input


def separate_rules_and_page_orders(lines: str) -> tuple[list[str], list[str]]:
    """Split input file on empty line."""
    rules_text, print_orders_text = lines.split("\n\n")
    return rules_text.splitlines(), print_orders_text.splitlines()


def parse_rules(rules: list[str]) -> list[tuple[int, int]]:
    rules = [rule.split("|") for rule in rules]
    return [(int(rule[0]), int(rule[1])) for rule in rules]


def filter_applicable_rules(
    rules: list[tuple[int, int]],
    page_orders: list[str],
) -> list[tuple[int, int]]:
    """Filter out rules that are not applicable to the print orders."""
    applicable_rules = []
    for rule in rules:
        for order in page_orders:
            if rule[0] not in order or rule[1] not in order:
                continue
            applicable_rules.append(rule)
            break

    return applicable_rules


def order_from_rules(rules: list[tuple[int, int]]) -> tuple[int]:
    """Return the order of pages from the rules."""
    graph = nx.DiGraph()
    graph.add_edges_from(rules)
    return tuple(nx.topological_sort(graph))


def parse_print_orders(print_orders: list[str]) -> list[tuple[int]]:
    """Convert list of strings to list of lists of integers.

    [["75, 47,..., 23"], ...] -> [[75, 47,..., 23], ...]
    """
    print_orders = [order.split(",") for order in print_orders]
    return [tuple(int(page) for page in orders) for orders in print_orders]


def order_is_ok(
    order: Iterable[int],
    allowed_page_order: Iterable[int],
) -> bool:
    """Check if the order is valid."""
    index_order = [allowed_page_order.index(p) for p in order]

    return index_order == sorted(index_order)


def get_middle_page_number(order: list[int]) -> int:
    """Return the middle page number in the order."""
    return order[len(order) // 2]


def correct_order(
    bad_orders: list[tuple[int]],
    allowed_orders: list[tuple[int]],
) -> list[tuple[int]]:
    corrected = []
    for bad, allowed in zip(bad_orders, allowed_orders, strict=False):
        index_order = [allowed.index(p) for p in bad]
        corrected.append(tuple(allowed[i] for i in sorted(index_order)))
    return corrected


if __name__ == "__main__":
    main()
