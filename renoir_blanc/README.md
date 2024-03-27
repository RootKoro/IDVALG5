# Renoir Blanc

IDV-ALGO5 | Etape 4 | Documentation

Ce programme a pour but de dessiner les contours d'une image de manière animée et réaliste avec l'algorithme de "Nearest Neighbore Search" en y applicant un flou grace aux algorithmes "Canny Edge detection" et "Gaussian blur" : lecture de l'image, détection des contours, application du flou, dessin animé de l'image.

## Requirements

- Python 3.x
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
python3 path/to/img_drawer.py -i|--image <image_path> -b|--blur <blur_type> [-k|--kernel <ksize>] [-s|--speed <speed>]
```
Avec :
- `blur_type` : `none`, `default`, `bilateral`, `gaussian`, `lens`, `linear`, `median`
- `ksize` : un entier strictement positif (`ksize > 0`) ; impaire pour les valeurs `median` et `gaussian` de blur_type
- `speed` : un entier compris entre `[0, 10]`


## Justification du choix

Le choix de `OpenCV` peut être justifié par:
- La documentation (accessible et à jour par rapport à la version) ;
- la communauté (grande, et présente) ;
- la renommée ;
- l'expérience (Certains d'entre nous ont déjà eu à utiliser `opencv` dans d'autres contextes).

Le choix de `scikit-learn` comme module s'explique simplement par la grande communauté, ainsi que son efficacité dans sa recherche de voisin.

## Explication de code

Le programme fonctionne comme suite:

1. Lecture de l'image à l'appelle du programme (`imread(self.img_path)`).
2. Application du flou choisi par l'utilisateur.
3. Calcule de la médiane (`median_value = median(img)`)..
4. Application de l'algorithme de détection des contours `Canny Edge Detection` (`Canny(img, median_value, 255)`).
5. Inversion de l'image trouvé après détection des contours (`bitwise_not(...)`).
6. Récupération des coordonnées des pixels n'appartenant pas à l'arrière plan
7. Initialisation d'un `KDTree` (organisation des pixels dans un espace k-dimensionnel)
8. Paramétrage de l'écran qui servira à afficher le dessin.
9. A partir du centre, application de l'algorithme de `Nearest Neighbore Search` afin de dessiner les contour pixel par pixel en se basant sur les pixels colorés les plus proches les uns des autres, pour lui donner un meilleur effet visuel
8. cacher les curseurs (tortues)

## Exemple

Structure de dossier:

    root
    |--renoir_blanc
    |----img_drawer.py
    |--assets
    |----licorne.png

à partir du répertoire root:

```bash
python3 renoir_blanc/img_drawer.py -i assets/licorne.png -b none -s 5
```