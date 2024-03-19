# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

import cv2
from numpy import median
from sys import argv


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 02
    Goal: Draw a sketch
    """

    def __init__(self, img_path: str, k_size: int):
        self.img_path = img_path
        self.k_size = (
            k_size if k_size % 2 != 0 and k_size > 0 else -1
        )  # Validate odd and positive kernel size

    def sketch_edge_drawer(self) -> None:
        """
        Reads the image, applies Gaussian blur (optional), calculates Canny edges,
        and displays the sketch.
        """

        try:
            img = cv2.imread(self.img_path)
            if self.k_size > 0:
                img = cv2.GaussianBlur(img, (self.k_size, self.k_size), 0)

            median_value = median(img)
            sketch_img = cv2.bitwise_not(
                cv2.Canny(img, median_value, 255)
            )  # Consider adjusting threshold

            cv2.imshow("sketch image", sketch_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        except (ValueError, IndexError) as e:
            print(f"Error: {e}")


def main():
    if len(argv) not in (2, 3):
        print("Usage: python sketch_drawer.py <image_path> [<kernel_size>]")
        return

    img_path = argv[1]
    try:
        kernel_size = int(argv[2] if len(argv) > 2 else -1)
    except ValueError:
        print("Invalid kernel size (must be a positive odd integer).")
        return

    svd = ImgDrawer(img_path, kernel_size)
    svd.sketch_edge_drawer()


if __name__ == "__main__":
    main()
