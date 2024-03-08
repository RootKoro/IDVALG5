# Big Fernand Leger

IDV-ALGO5 | Etape 2 | Documentation

Ce programme a pour but de dessiner les contours d'une image grace à l'algorithme "Canny Edge detection" : lecture de l'image, détectiond des contours, affichage des contours de l'image.

## Requirements

- Python 3.x
- opencv-python (cv2)
- numpy

## Usage

1. D'abord s'assurer d'avoir python d'installé sur son system, ou l'intaller;
2. Ensuite installer toutes les dépendances avec la commande suivante:
```bash
pip install -r requirements.txt
```
3. Exécuter le programme avec la commande:
```bash
python3 path/to/img_drawer.py <img_path>
```


## Justification du choix

Le choix de `OpenCV` peut être justifié par:
- La documentation (accessible et à jours par rapport à la version) ;
- la communauté (grande, et présente) ;
- la renommée ;
- l'expériece (Certains d'entre nous ont déjà eu à utiliser `opencv` dans d'autres contextes).

## Explication de code

Le programme fonctionne comme suite:

1. Lecture de l'image à l'appelle du programme (`img = imread(self.img_path)`).
    1. Si l'image n'existe pas ou a un mauvais format, une erreur est retournée.
2. Application des nuances de gris pour faciliter la détection de la médiane.
2. Calcule de la médiane (`median_value = median(img)`).
3. Application de l'algorithme de détection des contours `Canny Edge Detection` (`Canny(img, median_value, 255)`).
4. Inversion de l'image trouvé après détection des contours (`bitwise_not(...)`).
5. Affihchage de l'image (`imshow("sketch image", sketch_img)`).

## Exemple

Structure de dossier:

    root
    |--big_fernand_leger
    |----img_drawer.py
    |--assets
    |----licorne.png

à partir du répertoire root:

```bash
python3 big_fernand_leger/img_drawer.py assets/licorne.png
```