from __future__ import annotations

import pycuber as pc


def apply_scramble(scramble: str) -> pc.Cube:
    cube = pc.Cube()
    if scramble:
        cube(pc.Formula(scramble))
    return cube


