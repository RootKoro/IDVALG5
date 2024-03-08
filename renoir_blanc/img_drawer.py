# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

from sys import argv
from time import time
from turtle import Screen, Turtle, color, done, speed

from cv2 import (
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    Canny,
    GaussianBlur,
    bitwise_not,
    cvtColor,
    divide,
    imread,
)
from numpy import median
from sklearn.neighbors import KDTree


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 01
    Goal: Draw a sketch
    """

    img_path: str
    k_size: int
    screen: Screen
    drawer: Turtle

    def __init__(self, img_path: str, k_size: int | str, speed: int | str = 5):
        self.img_path = img_path
        self.k_size = int(k_size)
        self.speed = int(speed)
        self.drawer = Turtle()
        self.screen = Screen()

    def rgb_to_hex(self, r: int, g: int, b: int) -> None:
        """
        Convert RGB to hexadecimal color format (#RRGGBB).

        Args:
            r (int): Red value (0-255).
            g (int): Green value (0-255).
            b (int): Blue value (0-255).

        Returns:
            str: Hexadecimal color code in the format #RRGGBB.
        """
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def get_pixel_coords(self, img: any) -> list:
        """ """
        coords = []
        height = len(img)
        for y, line in enumerate(img):
            for x, value in enumerate(line):
                if value <= 127:
                    coords.append([x, height - y])
        return coords

    def sketch_edge_definer(self) -> any:
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
        5- return the new img corresponding to the new array
        """
        img = imread(self.img_path)
        if self.k_size > 0:
            img = GaussianBlur(img, (self.k_size, self.k_size), 0)
        median_value = median(img)

        return bitwise_not(Canny(img, median_value, 255))

    def sketch_drawer(self) -> any:
        img = self.sketch_edge_definer()
        coords = self.get_pixel_coords(img)
        tree = KDTree(coords)
        start = time()
        width = img.shape[1]
        height = img.shape[0]
        current = 0
        explored_ind = [0]

        self.screen.title("Zhang Gui")
        self.screen.screensize(width, height)
        self.screen.tracer(self.speed)
        self.drawer.hideturtle()
        self.drawer.penup()

        while len(coords) > 1:
            self.drawer.goto(
                coords[current][0] - (width / 2), coords[current][1] - (height / 2)
            )
            ind = tree.query_radius([coords[current]], r=1.42)
            ind = ind[0].tolist()
            ind = [value for value in ind if value not in explored_ind]

            if len(ind) >= 1:
                self.drawer.pendown()
                self.drawer.goto(
                    coords[ind[0]][0] - (width / 2), coords[ind[0]][1] - (height / 2)
                )
                self.drawer.penup()
                explored_ind.append(ind[0])
                current = ind[0]

            else:
                tmp = coords[current]
                coords = [
                    coords[i] for i in range(0, len(coords)) if i not in explored_ind
                ]
                explored_ind = []
                if len(coords) > 1:
                    tree = KDTree(coords)
                    _, i = tree.query([tmp], k=2)
                    i = i.flatten()
                    current = i[1]
        end = time()
        print("execution time : ", end - start)
        done()


def main():
    try:
        if len(argv) > 3 and int(argv[3]) in range(11):
            drawer = ImgDrawer(argv[1], argv[2], argv[3])
            drawer.sketch_edge_definer()
            drawer.sketch_drawer()
        else:
            raise Exception("")
    except Exception as e:
        print(e)
        print(
            "Please specify a valid image path, a valid odd kernel size and a speed between 0 and 10."
        )


if __name__ == "__main__":
    main()
