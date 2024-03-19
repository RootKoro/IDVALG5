<<<<<<< HEAD
# Sale Vador Dali

IDV-ALGO5 | Etape 2 | Documentation

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
# Big Fernand Leger

IDV-ALGO5 | Etape 1 | Documentation

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
>>>>>>> 5d073e7d437323003d09e49be75fae81574891a5
