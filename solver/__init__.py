from __future__ import annotations

from typing import List

from .kociemba_solver import KociembaSolver


SOLVERS = {
    'kociemba': KociembaSolver,
}


def get_solver(name: str = 'kociemba'):  # type: ignore
    solver_cls = SOLVERS.get(name)
    if not solver_cls:
        raise ValueError(f"Unknown solver {name}")
    return solver_cls()
