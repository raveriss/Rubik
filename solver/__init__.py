from .simple_solver import SimpleSolver


SOLVERS = {
    'simple': SimpleSolver,
}

def get_solver(name: str = 'simple'):  # type: ignore
    solver_cls = SOLVERS.get(name)
    if not solver_cls:
        raise ValueError(f"Unknown solver {name}")
    return solver_cls()
