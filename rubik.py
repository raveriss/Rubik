import sys
import time
_global_start = time.perf_counter()
import numpy as np

# Face notation: U, R, F, D, L, B
# Modifiers: 2 (double), ' (inverse)
VALID_MOVES = {f + m for f in ['U','R','F','D','L','B'] for m in ['', "2", "'"]}

class ParseError(Exception):
    pass

class Cube:
    """
    Simple cube engine storing sticker colors as integers 0..5 for faces.
    Faces are ordered U(0), R(1), F(2), D(3), L(4), B(5).
    Stickers stored as a list of length 54: 9 stickers per face.
    Movements are applied via precomputed mappings based on 3D rotation.
    """
    _face_order = ['U','R','F','D','L','B']
    _face_normals = {
        'U': np.array([0, 0, 1]),
        'D': np.array([0, 0, -1]),
        'F': np.array([0, 1, 0]),
        'B': np.array([0, -1, 0]),
        'R': np.array([1, 0, 0]),
        'L': np.array([-1, 0, 0]),
    }
    _sticker_coords = None
    _mappings = None

    @classmethod
    def _init_mappings(cls):
        if cls._mappings is not None:
            return
        
        # 1) Préparation du tableau de coordonnées (54 stickers × 3 axes)
        sticker_coords = np.zeros((54, 3))

        # Pour chaque face (U, R, F, D, L, B), on définit :
        # - N : la normale (direction) de la face
        # - T : un vecteur tangent (horizontale sur la face)
        # - B : un vecteur binormal (verticale sur la face)
        for fi, f in enumerate(cls._face_order):
            N = cls._face_normals[f] # vecteur normal unitaire de la face
            
            # Si la face est parallèle à l’axe Z, on prend X comme tangent par défaut
            if np.allclose(np.abs(N), np.array([0, 0, 1])):
                T = np.array([1, 0, 0])
            else:
                # Sinon, on croise Z et N pour obtenir un vecteur tangent
                T = np.cross(np.array([0, 0, 1]), N)
                T = T / np.linalg.norm(T) # normalisation
            B = np.cross(N, T) # binormal orthogonal à N et T
            # On calcule ensuite la position de chacun des 9 stickers de la face
            for p in range(9):
                r, c = divmod(p, 3)  # r = ligne (0 à 2), c = colonne (0 à 2)
                # pos = position centrale + décalages selon T et B
                pos = (
                    N * 1                   # on place la face à distance 1 de l’origine
                    + (c - 1) * (2/3) * T   # déplacement horizontal (écart de 2/3 unité)
                    + (1 - r) * (2/3) * B   # déplacement vertical inversé selon r
                )
                sticker_coords[fi*9 + p] = pos

        # Fonction auxiliaire pour retrouver l’indice du sticker le plus proche        
        def find_index(pos):
            dists = np.linalg.norm(sticker_coords - pos, axis=1)
            return int(np.argmin(dists))
        
        mappings = {}
        # 2) Pour chaque face, on pré-calcule la permutation induite par un quart de tour
        for f in cls._face_order:
            N = cls._face_normals[f]    # axe de rotation = normale de la face
            axis = N
            angle = -np.pi/2            # rotation de -90° (sens horaire vu de l’extérieur)

            # Matrice K pour le produit vectoriel en format matrice
            K = np.array([[0, -axis[2], axis[1]],
                          [axis[2], 0, -axis[0]],
                          [-axis[1], axis[0], 0]])
            
            # Formule de Rodrigues pour obtenir la matrice de rotation R
            R = np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * (K @ K)
            
            # On crée une mapping initial identique, qu’on va ajuster
            mapping = list(range(54))
            for i, pos in enumerate(sticker_coords):
                # Seuls les stickers sur la face f sont affectés (dot > 0.5)
                if np.dot(pos, N) > 0.5:
                    newpos = R @ pos                        # on fait tourner la coordonnée
                    j = find_index(np.round(newpos, 6))     # on retrouve l’indice cible
                    mapping[j] = i                          # on lie i → j
            mappings[f] = mapping

        # Stockage en classe pour réutilisation
        cls._sticker_coords = sticker_coords
        cls._mappings = mappings

    def __init__(self):
        Cube._init_mappings()
        self.state = [i // 9 for i in range(54)]

    def _permute(self, mapping):
        self.state = [self.state[mapping[i]] for i in range(54)]

    def apply_move(self, move):
        face = move[0]
        if face not in Cube._face_order:
            raise ParseError(f"Unknown face: {face}")
        times = 1
        if len(move) > 1:
            if move[1] == '2': times = 2
            elif move[1] == "'": times = 3
        for _ in range(times):
            self._permute(Cube._mappings[face])

    def apply_moves(self, moves):
        for mv in moves:
            self.apply_move(mv)

    def is_solved(self):
        return all(self.state[i] == self.state[9*(i//9)] for i in range(54))


def parse_mix(mix_str):
    if not mix_str:
        raise ParseError("Empty input mix.")
    tokens = mix_str.strip().split()
    for tok in tokens:
        if tok not in VALID_MOVES:
            raise ParseError(f"Invalid move token: {tok}")
    return tokens

# Two-phase solver inspired by Kociemba

# Phase 1 metrics: edge orientation (EO), corner orientation (CO), UD-slice edges index (UDS)
def heuristic_phase1(cube):
    # simple heuristic: count misoriented edges + misoriented corners
    # edges: positions [12,13,...] custom defined; here approximate by mismatched face centers
    mismatches = sum(1 for i in range(54) if cube.state[i] != cube.state[9*(i//9)])
    return mismatches // 8

# Phase 2 metric: remaining distance estimation (placeholder)
def heuristic_phase2(cube):
    return 0

MAX_DEPTH_PHASE1 = 7
MAX_DEPTH_PHASE2 = 10

def ida_star(cube, max_depth, heuristic, allowed_moves):
    path = []
    visited = set()
    def search(node, g, bound):
        f = g + heuristic(node)
        if f > bound: return f
        if heuristic(node) == 0:
            return True
        min_cost = float('inf')
        for mv in allowed_moves:
            cube2 = Cube()
            cube2.state = node.state.copy()
            cube2.apply_move(mv)
            key = tuple(cube2.state)
            if key in visited: continue
            visited.add(key)
            path.append(mv)
            t = search(cube2, g+1, bound)
            if t is True:
                return True
            if isinstance(t, int) and t < min_cost:
                min_cost = t
            path.pop()
            visited.remove(key)
        return min_cost

    bound = heuristic(cube)
    while True:
        t = search(cube, 0, bound)
        if t is True:
            return list(path)
        if t == float('inf'):
            return None
        bound = t

# Restrict moves: phase1 uses all face turns
ALL_MOVES = list(VALID_MOVES)
# Phase2 restricts to half-turn metric moves on slice moves simplified
PHASE2_MOVES = [m for m in ALL_MOVES if m[0] in ['U','D','R','L','F','B']]


def solve(mix_moves):
    # apply mix
    cube = Cube()
    cube.apply_moves(mix_moves)
    # Phase 1
    sol1 = ida_star(cube, MAX_DEPTH_PHASE1, heuristic_phase1, ALL_MOVES)
    if sol1 is None:
        raise RuntimeError("Phase 1 failed to find solution within depth")
    # apply phase1 moves
    cube.apply_moves(sol1)
    # Phase 2
    sol2 = ida_star(cube, MAX_DEPTH_PHASE2, heuristic_phase2, PHASE2_MOVES)
    if sol2 is None:
        raise RuntimeError("Phase 2 failed to find solution within depth")
    return sol1 + sol2

if __name__ == '__main__':
    start_time = time.time()
    if len(sys.argv) != 2:
        print("Usage: python rubik.py \"<mix sequence>\"")
        sys.exit(1)
    mix_input = sys.argv[1]
    try:
        mix_moves = parse_mix(mix_input)
    except ParseError as e:
        print(f"Error: {e}")
        sys.exit(1)

        # Chronomètre autour de la résolution
    start_time = time.time()
    solution = solve(mix_moves)
    elapsed = time.time() - start_time   

    solution = solve(mix_moves)
    print(' '.join(solution))
    print(f"Solved in {elapsed:.3f} seconds.")
    elapsed = time.time() - start_time
    if elapsed > 3.0:
        print("Warning: solving took longer than 3 seconds.", file=sys.stderr)
    # à la fin du main, après avoir affiché le solve et le chrono interne :
    _global_elapsed = time.perf_counter() - _global_start
    print(f"Total script time: {_global_elapsed:.3f} seconds.")
