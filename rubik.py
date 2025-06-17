#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
from typing import List

from solver import get_solver
from utils.cube_utils import apply_scramble


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rubik's cube solver")
    parser.add_argument("scramble", nargs="?", help="scramble sequence")
    parser.add_argument("--algo", default="simple", help="solver algorithm")
    parser.add_argument("--mix", type=int, default=0, help="generate random scramble of length")
    parser.add_argument("--ascii", action="store_true", help="display cube after scramble")
    return parser.parse_args()


def generate_scramble(length: int) -> str:
    moves = ['U', 'R', 'F', 'D', 'L', 'B']
    suffixes = ['', "'", '2']
    scramble = []
    last_move = None
    for _ in range(length):
        move = random.choice([m for m in moves if m != last_move])
        last_move = move
        scramble.append(move + random.choice(suffixes))
    return ' '.join(scramble)


def main() -> None:
    args = parse_args()
    scramble = args.scramble or ''
    if args.mix:
        scramble = generate_scramble(args.mix)
        print(f"Scramble generated: {scramble}")
    solver = get_solver(args.algo)
    if args.ascii:
        cube = apply_scramble(scramble)
        print(cube)
    solution: List[str] = solver.solve(scramble)
    print(' '.join(solution))


if __name__ == "__main__":
    main()
