# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

from numpy import median
from sys import argv

from cv2 import (
    COLOR_BGR2GRAY,
    GaussianBlur,
    Canny,
    cvtColor,
    bitwise_not,
    destroyAllWindows,
    imread,
    imshow,
    waitKey,
)


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 02
    Goal: Draw a sketch
    """

    img_path: str
    k_size: int

    def __init__(self, img_path: str, k_size: int):
        self.img_path = img_path
        self.k_size = k_size

    def sketch_edge_drawer(self) -> tuple:
        """
        1- Read the image
        2- Check if the k_size:
            a- k_size is given: image is blured with the gaussian algorithm
            b- k_size is not given: image is not blured, we go on the next step
        3- Get the median value of the img
            The image is converted into a 2 dimensional array of bits
            the median is retrieved from that array
        4- draw a new 2 dimensional array of bits containing the points
        retreived from the calculation of Canny algorithm
        5- Show the new img corresponding to the new array
        """
        img = imread(self.img_path)
        if self.k_size > 0:
            img = GaussianBlur(img, (self.k_size, self.k_size), 0)
        median_value = median(img)

        sketch_img = bitwise_not(Canny(img, median_value, 255))

        imshow("sketch image", sketch_img)
        waitKey(0)
        destroyAllWindows()


def main():
    try:
        if len(argv) == 2:
            svd = ImgDrawer(argv[1], -1)
        elif len(argv) > 2:
            svd = ImgDrawer(argv[1], int(argv[2]))
        else:
            raise Exception("")

        svd.sketch_edge_drawer()
    except:
        print(
            "Please specify a valid image path and a valid odd (fr. impaire) kernel size."
        )


if __name__ == "__main__":
    main()
