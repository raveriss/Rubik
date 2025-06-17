from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Cube:
    """Simple 3x3x3 Rubik's Cube representation."""

    faces: Dict[str, List[str]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.faces:
            self.faces = {f: [f] * 9 for f in "URFDLB"}

    def copy(self) -> "Cube":
        return Cube({f: s.copy() for f, s in self.faces.items()})

    def _rotate_face(self, face: str) -> None:
        """Rotate a face clockwise."""
        idx = [6, 3, 0, 7, 4, 1, 8, 5, 2]
        self.faces[face] = [self.faces[face][i] for i in idx]

    def _cycle(self, indices: List[tuple]) -> None:
        values = [self.faces[f][i] for f, i in indices]
        for (f, i), val in zip(indices, values[-1:] + values[:-1]):
            self.faces[f][i] = val

