# PyKart-maker
Comment créer facilement des cartes pour des jeux !

## Deck
Un deck est un json avec:
* name: le nom du Deck
* version: la version du deck (int)
* nbCarte: le nombre de cartes
* imgCarte: le path vers l'image de la cartes
* zone: une liste des zones sur la carte,
* Cartes: une liste des cartes et des différents attributs
* pdf (optionnel): Si on veut créer un pdf avec les différentes cartes
* * hmargin: marge horizontale
* * vmargin: marge vecticale
* * nb_h: nombre de carte sur une ligne
* * nb_v: nombre de carte sur une colonne

## Utilisation
Il faut tout d'abord definir les differentes zones

### Zones
#### Zones Texte
Une zone est définie par
* id
* type: "text"
* font: le lien vers le path du font
* Size: la taille du Texte
* R: composante rouge du Texte
* G: composante verte du Texte
* B: composante bleu du Texte
* xtop: la composante x à partir d'écrire
* ytop: la composante y à partir d'écrire
  
#### Zones image
Une Zone est définie par
* id
* type: "img"
* xtop: composante x du coin superieur gauche
* ytop: composante y du coin superieur gauche
* xbot: composante x du coin inferieur droit
* ybot: composante y du coin inferieur droit

### cartes
Une carte est definie par:
* nom: nom de la carte
* Pour chaque id des zones la valeur du text/le path vers l'image

## Build a deck
* `python main.py` va utiliser deck.json pour construire le deck
* `python main.py file.json' va utiliser file.json pour construire le deck

## Dépendances
Il y a le pipfile mais aussi:
* PIL: sudo apt install python-pil

## Version

* 1.2: Création d'un fichier pdf
* 1.1: restructuration + ajout de nom de deck pour build
* 1.0: Création de decks