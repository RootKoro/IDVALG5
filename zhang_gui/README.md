# Zhang GUI

IDV-ALGO5 | Etape 3 | Documentation

Ce programme a pour but de dessiner les contours d'une image de manière animée en y applicant un flou grace aux algorithmes "Canny Edge detection" et "Gaussian blur" : lecture de l'image, détection des contours, application du flou, dessin animé de l'image.

## Requirements

- Python 3.x
- opencv-python (cv2)
- turtle
- numpy

## Usage

1. D'abord s'assurer d'avoir python d'installé sur son system, ou l'intaller;
2. Ensuite installer toutes les dépendances avec la commande suivante:
```bash
pip install -r requirements.txt
```
3. Exécuter le programme avec la commande:
```bash
python3 path/to/img_drawer.py -i|--image <img_path> -b|--blur <blur_type> [-k|--kernel <ksize>] [-s|--speed <speed>]
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

## Explication de code

Le programme fonctionne comme suite:

1. Lecture de l'image à l'appelle du programme (`imread(self.img_path)`).
2. Application du flou choisi par l'utilisateur l'utilisateur.
3. Calcule de la médiane (`median_value = median(img)`).
4. Application de l'algorithme de détection des contours `Canny Edge Detection` (`Canny(img, median_value, 255)`).
5. Inversion de l'image trouvé après détection des contours (`bitwise_not(...)`).
6. Paramétrage de l'écran qui servira à afficher le dessin.
7. Pour chaque ligne de l'image (l'image considéré comme un tableau bidimentionnel (lignes + colones) de pixels) :
    1. Pour chaque pixel de cette ligne:
        1. Définir la position du pixel sur l'écran
        2. Récupérer la couleur du pixel
        3. Dessiner le pixel
    2. Mettre à jour le statut de l'écran
8. cacher les curseurs (tortues)

## Exemple

Structure de dossier:

    root
    |--zhang_gui
    |----img_drawer.py
    |--assets
    |----licorne.png

à partir du répertoire root:

```bash
python3 zhang_gui/img_drawer.py -i assets/licorne.png -b median -k 1 -s 10
```