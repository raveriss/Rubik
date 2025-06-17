from __future__ import annotations

import pycuber as pc

COLOR_MAP = {
    'yellow': 'U',
    'orange': 'R',
    'green': 'F',
    'white': 'D',
    'red': 'L',
    'blue': 'B',
}


def apply_scramble(scramble: str) -> pc.Cube:
    cube = pc.Cube()
    if scramble:
        cube(pc.Formula(scramble))
    return cube


def cube_to_kociemba(cube: pc.Cube) -> str:
    order = 'URFDLB'
    facelets = ''
    for face in order:
        for row in cube.get_face(face):
            for square in row:
                facelets += COLOR_MAP[square.colour]
    return facelets
