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
python3 path/to/img_drawer.py <img_path> <blur>
```


## Justification du choix

Le choix de `OpenCV` peut être justifié par:
- La documentation (accessible et à jour par rapport à la version) ;
- la communauté (grande, et présente) ;
- la renommée ;
- l'expérience (Certains d'entre nous ont déjà eu à utiliser `opencv` dans d'autres contextes).

Le choix de `Gaussian blur` se justifie par:
- contrairement au flou radial dont le flou crée un effet de rotation ou de tourbillonnement autour du centre de l'image, il applique un flou isotropique, ce qui signifie qu'il est appliqué uniformément dans toutes les directions ;
- Le flou encadré effectue des operations sur les pixels, nécessitant moins de ressources que le flou gaussien, mais ce dernier, même s'il applique un flou uniforme, pourrait produire des artéfacts visibles, notament sur les contours.

## Explication de code

Le programme fonctionne comme suite:

1. Lecture de l'image à l'appelle du programme (`img = imread(self.img_path)`).
    1. Si l'image n'existe pas ou a un mauvais format, une erreur est retournée.
2. Application du flou gaussien selon le choix de l'utilisateur.
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
python3 big_fernand_leger/img_drawer.py assets/lion.png 3
```