# Paulychrome Gauguin

IDV-ALGO5 | Etape 5 | Documentation

Dans cette étape, après avoir dessiner les contours de l'image, le programme devra 

Ce programme a pour but de dessiner les contours d'une image de manière animée et réaliste avec l'algorithme de "Nearest Neighbore Search" en y applicant un flou grace aux algorithmes "Canny Edge detection" et "Gaussian blur" : lecture de l'image, détection des contours, application du flou, dessin animé de l'image.

## Requirements

- Python 3.x
- _tkinter
- blurgenerator
- opencv-python (cv2)
- turtle
- numpy
- scikit-learn

## Usage

1. D'abord s'assurer d'avoir python d'installé sur son system, ou l'intaller;
2. Ensuite installer toutes les dépendances avec la commande suivante:
```bash
pip install -r requirements.txt
```
3. Exécuter le programme avec la commande:
```bash
python3 path/to/img_drawer.py -i|--image path/to/image -a|--algorithm algo -b|--blur blur_type [-k|--kernel ksize] -p|--palette color_palette [-s|--speed speed]
```
Avec :
- `algo` : `classification`, `clustering`
- `blur_type` : `none`, `default`, `bilateral`, `gaussian`, `lens`, `linear`, `median`
- `ksize` : un entier strictement positif (`ksize > 0`)
- `color_palette` : une liste json non limitée de couleurs sous forme `(r, g, b)`
- `speed` : un entier compris entre `[0, 10]`


## Justification du choix

Le choix de `OpenCV` peut être justifié par:
- La documentation (accessible et à jour par rapport à la version) ;
- la communauté (grande, et présente) ;
- la renommée ;
- l'expérience (Certains d'entre nous ont déjà eu à utiliser `opencv` dans d'autres contextes).

Le choix de `scikit-learn` comme module s'explique simplement par la grande communauté, son efficacité dans sa recherche de voisin facilité par le `k-dimentional tree` ; ainsi que son algorithme de clustering nous permettant dans notre cas de récupérer un palette de couleur appropriée grâce à son module `KDMeans`.

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
    9. A partir du centre, application de l'algorithme de `Nearest Neighbore Search` afin de dessiner les contour, pixel par pixel en se basant sur les pixels colorés les plus proches les uns des autres, pour lui donner un meilleur effet visuel
5. Choix d'une palette de couleur en fontion de l'algorithm choisi par l'utilisateur
6. Traitement de l'image à 3 dimensions pour la painture des couleurs
    1. Réadaptation de l'image en fonction de la palette de couleur choisie (les couleurs de l'image risquent d'être modifier pour lui donner une touche artistique)
    2. Réutilisation de l'algorithme de `Nearest Neighbore Search` pour peindre les couleur sur l'image


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