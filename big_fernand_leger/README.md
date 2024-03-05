# BIG FERNAND LEGER

IDV-ALGO5 | Etape 1 | Documentation

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
Ensuite, ces arguments sont directement passé à la classe afin de permettre les manipulation suivantes:
- d'abord l'image subira sa première transformation (grisaye + inversion de l'image grisé)
- ensuite vient la seconde transformation (floutage + seconde inversion de l'image flouté)
Cela est fait de sorte à avoir deux image, la première transformation et la seconde transformation issue de la première.
- Ensuite les deux images sont alors convertis en une seule image par `divide` qui tout simplement va faire une opération de division par bit afin d'obtenir une image à partir des deux précédentes, et cet image est le resultat dont nous avons besoin.
- Cet image sera ensuite affiché à l'écran