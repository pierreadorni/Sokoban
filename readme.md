# Sokoban Solver

## Installation 

Nécessite python 3.6 ou supérieur.

Clonez le repo, puis installez les dépendances avec `pip`:
```bash
pip install -r requirements.txt
```

## Utilisation
un exemple d'utilisation du module *Sokoban* est fourni dans le fichier `example.py`.

### Classe State: Modèle

La classe State sert de modèle pour les états du jeu.
Elle est initialisée en lui passant en argument un *string* représentant l'état du jeu.

Ce string doit être composé des caractères suivants:

| Caractère | Signification    |
|-----------|------------------|
| %         | mur              |
| espace    | vide             |
| p         | joueur           |
| c         | caisse           |
| b         | but              |
| v         | caisse sur un but |
| q         | joueur sur un but |

```python
from sokoban import State

state_string = \
"""
%%%%
%p %
%c %
%b %
%%%%
"""

initial_state = State(state_string)
```

### La classe Sokoban: Contrôleur

La classe Sokoban est une collection de méthodes pour manipuler les états du jeu.

```python
from sokoban import Sokoban

sokoban = Sokoban(initial_state)
print(sokoban.current_state)

sokoban.execute("Bd")
print(sokoban.current_state)
```

La fonction `execute` ci dessus exécute une suite d'actions, représentée par un string composé des caractères suivants:

| Caractère | Signification                   |
|-----------|---------------------------------|
| h         | se déplacer vers le haut        |
| b         | se déplacer vers le bas         |
| g         | se déplacer vers la gauche      |
| d         | se déplacer vers la droite      |
| H         | déplacer la caisse vers le haut |
| B         | déplacer la caisse vers le bas  |
| G         | déplacer la caisse vers la gauche|
| D         | déplacer la caisse vers la droite|

### La classe Visualizer: Vue

La classe Visualizer est une collection de méthodes pour afficher les états du jeu.
Elle utilise le module `pygame` pour l'affichage.

```python
from sokoban import Visualizer

Visualizer(sokoban).show_history()
```
