# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

from numpy import median
from sys import argv

from cv2 import (
    COLOR_BGR2GRAY,
    Canny,
    bitwise_not,
    cvtColor,
    destroyAllWindows,
    imread,
    imshow,
    waitKey,
)


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 01
    Goal: Draw a sketch
    """

    img_path: str

    def __init__(self, img_path: str):
        self.img_path = img_path

    def sketch_edge_drawer(self) -> tuple:
        """
        1- Read the image
        2- turn the img into a gray image
        3- Get the median value of the img
            the image is converted into a 2 dimensional array of bits
            the median is retrieved from that array
        4- draw a new 2 dimensional array of bits containing the points
            retreived from the calculation of Canny algorithm
        5- Show the new img corresponding to the new array
        """
        img = imread(self.img_path)
        gray_img = cvtColor(img, COLOR_BGR2GRAY)
        median_value = median(gray_img)

        sketch_img = bitwise_not(Canny(gray_img, median_value, 255))

        imshow("sketch image", sketch_img)
        waitKey(0)
        destroyAllWindows()


def main():
    try:
        if len(argv) > 1:
            bfl = ImgDrawer(argv[1])
            bfl.sketch_edge_drawer()
        else:
            raise Exception("")
    except:
        print("""Please specify a valid image path and a kernel size.""")


if __name__ == "__main__":
    main()
