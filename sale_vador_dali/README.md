# Sale Vador Dali

IDV-ALGO5 | Etape 2 | Documentation

<<<<<<< HEAD
## Installation des dépendances requises
```bash
pip install -r requirements.txt
```

## Dépendances requises
`opencv-python`

## Usage
```bash
python3 img_drawer.py /path/to/img.png 9
```

## Justification du choix

Nous avons choisi cette librairie plus précisément parmi les autres, principalement car elle a plus d'exemple d'illustration, est très bien documentée et est bien reconnu du grand public.

## Explication du déroulement

Le program est structuré en classe pour faciliter son utilisation.

Sachant que les arguments sont attendus en ligne de commande, le première chose à faire est de vérifier si l'ensemble des arguments a bien été entré.
- le premier argument représente le chemin absolu de l'image
- le second argument représente le degrès de floutage à apporter à l'image (proportionnel à la taille de l'image)

Ensuite, ces arguments sont directement passé à la classe afin de permettre les manipulation suivantes:
- d'abord l'image subira sa première transformation (grisaye + inversion de l'image grisé)
- ensuite vient la seconde transformation (floutage + seconde inversion de l'image flouté)
Cela est fait de sorte à avoir deux image, la première transformation et la seconde transformation issue de la première.
- Ensuite les deux images sont alors convertis en une seule image par `divide` qui tout simplement va faire une opération de division par bit afin d'obtenir une image à partir des deux précédentes, et cet image est le resultat dont nous avons besoin.
- Cet image sera ensuite affiché à l'écran
=======
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
python3 sale_vador_dali/img_drawer.py assets/lion.png 3
```
>>>>>>> 5d073e7d437323003d09e49be75fae81574891a5
