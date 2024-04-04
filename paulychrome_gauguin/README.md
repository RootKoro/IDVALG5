# Paulychrome Gauguin

IDV-ALGO5 | Etape 5 | Documentation

Dans cette étape, après avoir dessiner les contours de l'image, le programme devra 

Ce programme a pour but de dessiner les contours d'une image de manière animée et réaliste avec l'algorithme de "Nearest Neighbore Search" en y applicant un flou grace aux algorithmes "Canny Edge detection" et "Gaussian blur" : lecture de l'image, détection des contours, application du flou, dessin animé de l'image.

## Abréviations

- `KDTree` = `k-dimentional tree`
- `NNS` = `Nearest Neightbore Search`

## Requirements

- Python 3.x
- opencv-python (cv2)
- turtle
- numpy
- scikit-learn

## Usage

1. D'abord s'assurer d'avoir python d'installé sur son system, ou l'intaller;
2. Ensuite installer toutes les dépendances avec la commande suivante:
On Windows:
```powershell
python -m venv algo-env
.\algo-env\Scripts\activate
pip install -r requirements.txt
```
On linux.
```bash
python -m venv algo-env
source ./algo-env/bin/activate
pip install -r requirements.txt
```

3. Exécuter le programme avec la commande:
```bash
python3 path/to/img_drawer.py -i|--image path/to/image [-s|--speed speed]
```
Avec :
- `speed` : un entier compris entre `[0, 10]` correspondant à la vitesse avec laquelle sera paint l'image. Entre `1` et `10` la vitesse aumente graduellement, avec `1` le plus petite vitesse ; cependant la plus grande vitesse sera `0`.


## Justification de choix

Le choix de `OpenCV` peut être justifié par:
- La documentation (accessible et à jour par rapport à la version) ;
- la communauté (grande, et présente) ;
- la renommée ;
- l'expérience (Certains d'entre nous ont déjà eu à utiliser `opencv` dans d'autres contextes).

Après avoir comparé plusieurs flou, avec plus ou moins le même résultat (`bilateral`, `gaussian`, `lens`, `linear`, `median`), nous avons décidé de creuser peu plus afin d'obtenir des raisons de choisir un flou bien précis:
- le flou `bilateral` effectue un flou sur l'image tout en préservant les contours net et intactes, dans le sens où tous les contours ne devraient pas être dessinés, celui là ne serait pas le meilleur choix à faire ;
- le flou de `lens` imite l'effet de flou causé par une lentille d'appareil photo, souvent utilisé pour simuler la profondeur de champ en photographie, ce qui ne correspond pas vraiment à nos attentes ;
- le flou `lineaire` a pour effet d'appliquer des filtres sur une ligne droite ;
- le flou `median` remplace chque pixel par la valeur median des pixels aux alentours (ce qui n'est pas non plus notre but)
- le flou `Gaussien` cependant applique un flou général et uniforme sur l'image afin de diminuer l'intensité des détails à récupérer, en fonction d'un poid moyen sur les pixels voisins, ce qui permet de retrouver une image assez flou (en fonction de la valeur qui lui sera passée) pour retrouver les contours qui nous intéressent pour dessiner notre `sketch`.

Ce qui explique le choix du flou `gaussien` avec une valeur de 3 comme kernel, un juste milieu pour acquérir une bonne image avec les images à faible intensité comme pour les images très intenses.

Pourquoi avoir choisi `Canny edge detection` comme algorithme de détection des contours au lieu d'un autre algorithme?
- Contrairement aux autres, il comprend plusieurs étape telles que le calcul du gradient, la suppression des non-maxima ainsi que l'application d'un `thresholding` ; afin de fariner l'image et d'ignorer les détails inutils.
- Il utilise un `thresholding` adaptif pour différencier les vrai contours de l'image des détails présent dans l'image ; ce qui résulte à une détection assez précise des contours de manière nette.
- Sa marge d'erreur est très faible.

Le choix de `scikit-learn` comme module s'explique simplement par la grande communauté, son efficacité dans sa recherche de voisin facilité par le `KDTree` ; ainsi que son algorithme de clustering nous permettant dans notre cas de récupérer un palette de couleur appropriée grâce à son module `KDMeans`.
- Le `KDTree` permet de représenter les pixels sur un plan à K dimensions, afin de pouvoir repérer les pixels voisins de manière plus efficace en fonction de leurs positions ainsi que de leur similitude. Cela nous permet d'utiliser le `NNS` afin de repérer les pixels les plus proches les uns des autres pour produire une animation assez réaliste, comme si le dessin se faisait par une main, en live.
- Le `KDMeans` permet, toujours dans un plan à K dimension, de retrouver les pixels se rapprochant par couleurs, afin de les regrouper par groupe, ce qui nous permet, dans ce cas, de récuper la couleur représentative de chaque groupe, obtenant ainsi une palette des couleurs dominantes de l'image.

## Explication de code

Le programme fonctionne comme suite:

1. Paramétrage de l'écran qui servira à afficher le dessin.
2. Lecture de l'image en 2 dimentions (pour la représentation des contours) et en 3 dimentions (pour la painture des couleurs).
3. cacher les curseurs (tortues)
4. Traitement de l'image à 2 dimentions pour la représentation des contours:
    1. Application du flou choisi par l'utilisateur.
    2. Calcule de la médiane.
    3. Application de l'algorithme de détection des contours `Canny Edge Detection`
    4. Inversion de l'image retourné après détection des contours.
    5. Récupération des coordonnées des pixels n'appartenant pas à l'arrière plan
    6. Initialisation d'un `KDTree` (organisation des pixels dans un espace k-dimensionnel)
    9. A partir du centre, application de l'algorithme de `Nearest Neightbore Search` afin de dessiner les contour, pixel par pixel en se basant sur les pixels colorés les plus proches les uns des autres, pour lui donner un meilleur effet visuel
5. Choix d'une palette de couleur en fontion de l'algorithm choisi par l'utilisateur
6. Traitement de l'image à 3 dimensions pour la painture des couleurs
    1. Réadaptation de l'image en fonction de la palette de couleur choisie (les couleurs de l'image risquent d'être modifier pour lui donner une touche artistique)
    2. Réutilisation de l'algorithme de `Nearest Neightbore Search` pour peindre les couleur sur l'image


## Exemple

Structure de dossier:

    root
    |--paulychrome_gauguin
    |----img_drawer.py
    |--assets
    |----lion.jpg

à partir du répertoire root:

```bash
python3 paulychrome_gauguin/img_drawer.py -i assets/lion.jpg -a clustering -b default -s 10
```