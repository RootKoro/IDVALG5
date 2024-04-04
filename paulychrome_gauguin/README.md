# Paulychrome Gauguin

IDV-ALGO5 | Etape 5 | Documentation

Dans cette étape, après avoir dessiner les contours de l'image, le programme devra 

Ce programme a pour but de peindre une image de manière animée et réaliste grâce aux algorithmes de `Gaussien blur` pour y appliquer un flou homogène, de `Canny Edge Detection` afin d'en déterminer les contours, de `clustering` dans le but de déterminer une palette de couleur pour la peinture, et de `Nearest Neighbor Search` afin de déterminer l'ordre de dessin des pixels.

## Abréviations

- `KDTree` = `k-dimentional tree`
- `NNS` = `Nearest Neightbore Search`
- `Canny Edge Detection` = `CED`

## Requirements

- Python 3.x
- opencv-python (cv2)
- turtle
- numpy
- scikit-learn

## Usage

1. D'abord s'assurer d'avoir python d'installé sur son system, ou l'intaller;
2. Ensuite installer toutes les dépendances avec la commande suivante:
- Sur Windows:
```powershell
python -m venv algo-env
.\algo-env\Scripts\activate
pip install -r requirements.txt
```
- Sur linux.
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
- `speed` : un entier compris entre `[0, 10]` correspondant à la vitesse avec laquelle sera peint l'image. Entre `1` et `10` la vitesse augmente graduellement, avec `1` la plus petite vitesse ; cependant, la plus grande vitesse sera `0`.


## Justification de choix

Le choix de `OpenCV` peut être justifié par :
- La documentation (accessible et à jour par rapport à la version) ;
- la communauté (grande, et présente) ;
- la renommée ;
- l'expérience (Certains d'entre nous ont déjà eu à utiliser `opencv` dans d'autres contextes).

Après avoir comparé plusieurs flous, avec plus ou moins le même résultat (`bilateral`, `gaussian`, `lens`, `linear`, `median`), nous avons décidé de creuser peu plus afin d'obtenir des raisons de choisir un flou bien précis:
- le flou `bilateral` effectue un flou sur l'image tout en préservant les contours nets et intacts, dans le sens où tous les contours ne devraient pas être dessinés, celui-là ne serait pas le meilleur choix à faire ;
- le flou de `lens` imite l'effet de flou causé par une lentille d'appareil photo, souvent utilisé pour simuler la profondeur de champ en photographie, ce qui ne correspond pas vraiment à nos attentes ;
- le flou `lineaire` a pour effet d'appliquer des filtres sur une ligne droite ;
- le flou `median` remplace chaque pixel par la valeur médian des pixels aux alentours (ce qui n'est pas non plus notre but)
- le flou `Gaussien` cependant applique un flou général et uniforme sur l'image afin de diminuer l'intensité des détails à récupérer, en fonction d'un poids moyen sur les pixels voisins, ce qui permet de retrouver une image assez flou (en fonction de la valeur qui lui sera passée) pour retrouver les contours qui nous intéressent pour dessiner notre `sketch`.

Ce qui explique le choix du flou `gaussien` avec une valeur de 3 comme kernel, un juste-milieu pour acquérir une bonne image avec les images à faible intensité comme pour les images très intenses.

Pourquoi avoir choisi `CED` comme algorithme de détection des contours au lieu d'un autre algorithme ?
- Contrairement aux autres, il comprend plusieurs étapes telles que le calcul du gradient, la suppression des non-maxima ainsi que l'application d'un `thresholding` ; afin de fariner l'image et d'ignorer les détails inutiles.
- Il utilise un `thresholding` qui s'adapte pour différencier les vrais contours de l'image des détails présents dans l'image ; ce qui résulte à une détection assez précise des contours de manière nette.
- Sa marge d'erreur est très faible.

Le choix de `scikit-learn` comme module s'explique simplement par la grande communauté, son efficacité dans sa recherche de voisin facilité par le `KDTree` ; ainsi que son algorithme de `clustering` nous permettant dans notre cas de récupérer une palette de couleur appropriée grâce à son module `KDMeans`.
- Le `KDTree` permet de représenter les pixels sur un plan à K dimensions, afin de pouvoir repérer les pixels voisins de manière plus efficace en fonction de leurs positions ainsi que de leur similitude. Cela nous permet d'utiliser le `NNS` afin de repérer les pixels les plus proches les uns des autres pour produire une animation assez réaliste, comme si le dessin se faisait à la main et en live.
- Le `KDMeans` permet, toujours dans un plan à K dimension, de retrouver les pixels se rapprochant par couleurs, afin de les regrouper par groupe, ce qui nous permet, dans ce cas, de récupérer la couleur représentative de chaque groupe, obtenant ainsi une palette des couleurs dominantes de l'image.

## Explication de code

1. D'abord, nous paramétrons la fenêtre d'affichage de notre œuvre d'art (longueur, largeur, titre de la fenêtre, couleur du curseur, vitesse de dessin, ...).
2. Deux lectures différentes de l'image à peindre : 
- Une lecture 2D que nous nommerons `I2D` pour le dessin des contours ; 
- Une lecture 3D nommée `I3D` pour la peinture des couleurs.
3. Nous allons maintenant passer au dessin des contours.
    1. On commence par appliquer le flou `gaussien` sur `I2D`, afin de nous débarrasser de tout détail qui pourrait gêner la détection des contours.
    2. Ensuite, on applique l'algorithme de `CED` qui nous permet, à partir du flou récupéré de `I2D`, de détecter les contours de l'image afin de les dessiner le plus fidèlement possible.
    3. Cependant, après avoir appliqué `CED`, nous nous retrouvons avec une image sombre avec les contours clairs, il faudra donc inverser les couleurs afin d'obtenir un arrière-plan clair avec des contours noirs ; ce qui nous amène à utiliser `bitwise_not` qui nous est directement fourni par la bibliothèque `opencv-python`.
    4. Nous récupérons ensuite les coordonnées de chaque pixel constituant les contours que nous placerons dans un espace k-dimensionnel afin de pouvoir appliquer sur eux l'algorithme de `NNS` pour déterminer quel pixel sera représenté en premier, et lequel suivra. Cet algorithme permet de retrouver le plus proche voisin d'un élément, ce qui nous permet, dans notre cas, de pouvoir dessiner, pas de manière aléatoire, mais de manière artistique les contours de notre image.
4. Pour le choix de la palette de couleur, nous avons décidé d'utiliser l'algorithme de `clustering`, car contrairement à la `classification` où nous sommes obligés d'avoir une palette prédéfinie (ce qui pourrait mener à une mauvaise, voir infidèle représentation des couleurs de l'image), elle extrait directement de l'image un nombre déterminé de couleur (cf. `justification des choix`).
5. Ensuite, vient la phase de réadaptation de l'image en fonction des couleurs déterminées par la palette ; les pixels de l'image sont chacun modifié pour prendre les couleurs qui leur sont les plus proches dans la palette déterminée ; puis on applique l'algorithme de `NNS` avec chaque couleur de la palette afin de peindre l'image de manière fidèle et artistique.


## Exemple

Structure de dossier:

    root
    |--paulychrome_gauguin
    |----img_drawer.py
    |--assets
    |----lion.jpg

à partir du répertoire root:

```bash
python3 paulychrome_gauguin/img_drawer.py -i assets/lion.jpg -s 10
```