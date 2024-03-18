# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA
# Licenceless

from numpy import median
from sys import argv

from cv2 import (
    Canny,
    bitwise_not,
    destroyAllWindows,
    imread,
    imshow,
    waitKey,
)

CMD = ("-i", "--image")


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
        3- Get the median value of the img
            the image is converted into a 2 dimensional array of bits
            the median is retrieved from that array
        4- draw a new 2 dimensional array of bits containing the points
            retreived from the calculation of Canny algorithm
        5- Show the new img corresponding to the new array
        """
        img = imread(self.img_path)
        median_value = median(img)

        sketch_img = bitwise_not(Canny(img, median_value, 255))

        imshow("sketch image", sketch_img)
        waitKey(0)
        destroyAllWindows()


def help_menu():
    print("Usage:\n")
    print("img_drawer.py [-h|--help]")
    print("img_drawer.py [-i|--image] path/to/image")


def is_valid(cmd: str) -> bool:
    """ """
    global CMD
    return True if cmd in CMD else False


def main():
    try:
        if len(argv) > 2 and is_valid(argv[1]):
            ...
        else:
            raise Exception
    except Exception:
        help_menu()


if __name__ == "__main__":
    main()
