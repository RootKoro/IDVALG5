# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
import numpy as np
import cv2
from sklearn.neighbors import KNeighborsClassifier

def colorize_classification(sketch_path, palette):
    """
    Colorizes a sketch using K-Nearest Neighbors classification.

    Args:
        sketch_path: Path to the sketch image.
        palette: List of colors (BGR tuples) to use for classification.
    """
    # Load sketch and convert to LAB color space
    sketch = cv2.imread(sketch_path, cv2.IMREAD_COLOR)  # Charger l'image avec cv2.IMREAD_COLOR
    sketch_lab = cv2.cvtColor(sketch, cv2.COLOR_BGR2LAB)

    # Reshape sketch for KNN
    sketch_data = sketch_lab.reshape((-1, 3))

    # Create KNN model with chosen palette colors as training data
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(np.array(palette), np.arange(len(palette)))  # Utilisation de np.arange ici

    # Predict color labels (indices in the palette) for each pixel
    labels = knn.predict(sketch_data)

    # Convert labels to integers
    labels = labels.astype(int)

    # Reshape labels to image format and convert color space back to BGR
    colored_img = np.array([palette[label] for label in labels]).reshape(sketch.shape)
    colored_img = cv2.cvtColor(colored_img, cv2.COLOR_LAB2BGR)

    return colored_img

# Example usage
palette = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Simple red, green, blue palette
colored_img = colorize_classification("lion.jpg", palette)
cv2.imshow("Colorized Image (Classification)", colored_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
