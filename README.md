# rubik 🎯🧩

Résolveur de Rubik’s Cube en Python – calcule la solution la plus courte à partir d’une séquence de mélange, selon le format officiel HTM (Half-Turn Metric), en moins de 3 secondes.

<div align="center">
  <img src="https://img.shields.io/badge/status-en%20cours-orange" alt="Status" />
  <img src="https://img.shields.io/badge/python-3.10+-blue" alt="Python" />
  <img src="https://img.shields.io/badge/licence-MIT-green" alt="Licence MIT" />
</div>


---

## Table des matières

- [🧠 Contexte du projet](#-contexte-du-projet)
- [🔧 Prérequis](#-prérequis)
- [⚙️ Installation](#️-installation)
- [🚀 Utilisation](#-utilisation)
- [🗂 Structure du dépôt](#-structure-du-dépôt)
- [✅ Fonctionnalités obligatoires & bonus](#-fonctionnalités-obligatoires--bonus)
- [📌 Bonnes pratiques d’exploitation](#-bonnes-pratiques-dexploitation)
- [🤝 Contribution](#-contribution)
- [📄 Licence](#-licence)
- [👤 Crédits & contact](#-crédits--contact)

---

## 🧠 Contexte du projet

Ce projet de l’école 42 vous invite à implémenter un **résolveur automatique** de Rubik’s Cube 3x3x3, à partir d’un **mélange prédéfini** en notation officielle (F, R, U, B, L, D), et à en fournir la **solution minimale** en nombre de mouvements HTM.

Inspiré des compétitions **FMC (Fewest Moves Challenge)**, l’objectif est de trouver un algorithme efficace, rapide et rigoureux.

---

## 🔧 Prérequis

- Python ≥ **3.10**
- Aucune dépendance externe obligatoire, mais vous pouvez utiliser (justifié) :
  - `numpy` pour la manipulation de l’état du cube
  - `argparse` ou `click` pour l’interface CLI
  - `colorama` (bonus visuel en CLI)

---

## ⚙️ Installation

Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/<votre_utilisateur>/rubik.git
cd rubik
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Lancez ensuite le script :

```bash
python rubik.py "F R U2 B' L' D'"
```
## 🚀 Utilisation
```bash
python rubik.py "R2 U' B L2 F D2 R U"
```
Affiche une solution optimisée :

```bash
L2 U' F2 B R' D'
```
## 📏 Pour connaître le nombre de coups :

```bash
python rubik.py "R2 U' B L2 F D2 R U" | wc -w
```
## 🗂 Structure du dépôt
```bash
rubik/
├── rubik.py            # Script principal
├── cube.py             # Modèle de Rubik's Cube
├── solver/             # Algorithmes de résolution
│   ├── idastar.py
│   └── bruteforce.py
├── utils/              # Outils d’analyse, parsing, affichage
├── tests/              # Tests unitaires
├── requirements.txt    # Dépendances Python
├── README.md
└── LICENSE
```
## ✅ Fonctionnalités obligatoires & bonus
### Obligatoire
✔ Lecture d’une séquence de spins
✔ Représentation interne du cube (3D ou simplifiée)
✔ Affichage de la solution optimisée en notation HTM
✔ Temps de calcul < 3 secondes
✔ Longueur moyenne de solution ≤ 50 coups

### Bonus
🎨 Visualisation ASCII ou curses du cube
🧠 Plusieurs algorithmes au choix (`--algo`)
🧪 Générateur de scramble intégré (`--mix 20`)
📊 Analyse comparative de solutions
🔄 Support du cube 2x2x2 (`--variant 2x2`)
📚 Décomposition pédagogique de la résolution (`--explain`)

## 📌 Bonnes pratiques d’exploitation
- Gestion robuste des erreurs d’input (mauvaise syntaxe, spins non autorisés)
- Interdiction d’inverser naïvement la séquence de mélange
- Respect strict de la **notation standard**
(F, R, U, B, L, D avec suffixes `'`, `2`)
- Algorithmes optimisés : IDA*, BFS amélioré, heuristiques admissibles

## 🤝 Contribution
Envie de contribuer ?

```bash
git clone https://github.com/<votre_utilisateur>/rubik.git
git checkout -b feature/ma-fonction
```
Merci de respecter :
- [PEP8](https://peps.python.org/pep-0008/) pour le style
- Ajoutez des tests dans `tests/`
- Documentez toute nouvelle fonctionnalité

## 📄 Licence
Ce projet est sous licence [MIT](./LICENSE)

## 👤 Crédits & contact
Auteur : VERISSIMO

École : 42 Paris

Mail : raveriss@student.42.fr

> "Un cube peut être résolu en 20 mouvements. Mais votre code peut-il le faire en 3 secondes ?”
> 
> — FMC Philosophy
