# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA
# Licenceless

from numpy import median
from os.path import exists
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

    def sketch_edge_drawer(self, image_path: str) -> None:
        """
        1- Read the image
        2- Get the median value of the img
            the image is converted into a 2 dimensional array of bits
            from which the median value of bits is retreived
        3- From Canny edge detection and threshold calculation defining
            a two dimentionnal array of point corresponding to the sketch
        4- Show the new img corresponding to the new array
        """
        img = imread(image_path)
        median_value = median(img)
        sketch_img = bitwise_not(Canny(img, median_value, 255))

        imshow("sketch image", sketch_img)
        waitKey(0)
        destroyAllWindows()


def help_menu():
    print("Usage:")
    print("img_drawer.py [-h|--help]")
    print("img_drawer.py [-i|--image] path/to/image")


def is_valid(cmd: str) -> bool:
    """ """
    global CMD
    return True if cmd in CMD else False


def main():
    try:
        if len(argv) > 2 and is_valid(argv[1]):
            if exists(argv[2]):
                bfl = ImgDrawer()
                bfl.sketch_edge_drawer(str(argv[2]))
            else:
                print("Error:: File does not exist !")
        else:
            raise Exception
    except TypeError:
        print("Unsupported type of file given !")
    except Exception as e:
        help_menu()


if __name__ == "__main__":
    main()
