"""Command-line interface for the modular linear system solver."""

import argparse
import sys
from typing import List

from solver.alg import get_input, solve_modular_system


def read_matrix_from_file(f) -> List[List[int]]:
    """Read augmented matrix from a text file-like object.

    Each line should contain whitespace-separated integers representing a
    single row of the augmented matrix.  Empty lines and comments (#)
    are ignored.
    """

    matrix = []
    for raw in f:
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        try:
            row = [int(x) for x in parts]
        except ValueError:
            raise ValueError(f"non-integer value in matrix: {line}")
        matrix.append(row)
    return matrix


def parse_args():
    parser = argparse.ArgumentParser(
        description="Solve a system of linear equations modulo a prime."
    )
    parser.add_argument(
        "-p",
        "--prime",
        type=int,
        required=True,
        help="prime modulus (must be a positive prime integer)",
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-f",
        "--file",
        type=argparse.FileType("r"),
        help="text file containing augmented matrix",
    )
    group.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="prompt for matrix entry interactively",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.file:
        matrix = read_matrix_from_file(args.file)
    elif args.interactive or sys.stdin.isatty():
        # ask user for dimensions
        num_coef = int(input("number of coefficients per row (variables+1): "))
        num_eq = int(input("number of equations: "))
        matrix = get_input(num_coef, num_eq)
    else:
        # allow reading from stdin if piped
        matrix = read_matrix_from_file(sys.stdin)

    try:
        result = solve_modular_system(matrix, args.prime)
    except Exception as ex:  # pylint: disable=broad-except
        print(f"error: {ex}")
        sys.exit(1)

    print("solution:", result)


if __name__ == "__main__":
    main()
