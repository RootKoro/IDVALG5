# Sale Vador Dali

IDV-ALGO5 | Etape 2 | Documentation

Ce programme a pour but de dessiner les contours d'une image en y applicant un flou grace aux algorithmes "Canny Edge detection" et "Gaussian blur" : lecture de l'image, détection des contours, application du flou, affichage des contours de l'image.

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
python3 path/to/img_drawer.py -i|--image <img_path> -b|--blur <blur_type> -k|--kernel <ksize>
```
Avec :
- `blur_type` : `none`, `default`, `bilateral`, `gaussian`, `lens`, `linear`, `median`
- `ksize` : un entier strictement positif (`ksize > 0`) ; impaire pour les valeurs `median` et `gaussian` de blur_type


## Justification du choix

Le choix de `OpenCV` peut être justifié par:
- La documentation (accessible et à jour par rapport à la version) ;
- la communauté (grande, et présente) ;
- la renommée ;
- l'expérience (Certains d'entre nous ont déjà eu à utiliser `opencv` dans d'autres contextes).

## Explication de code

Le programme fonctionne comme suite:

1. Lecture de l'image à l'appelle du programme (`imread(img_path)`).
2. Application du flou choisi par l'utilisateur
3. Calcule de la médiane (`median_value = median(img)`).
4. Application de l'algorithme de détection des contours `Canny Edge Detection` (`Canny(img, median_value, 255)`).
5. Inversion de l'image trouvé après détection des contours (`bitwise_not(...)`).
6. Affichage de l'image (`imshow("sketch image", sketch_img)`).

## Exemple

Structure de dossier:

    root
    |--sale_vador_dali
    |----img_drawer.py
    |--assets
    |----licorne.png

à partir du répertoire root:

```bash
python3 sale_vador_dali/img_drawer.py -i assets/lion.png -b gaussian -k 3
```
