# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

from sys import argv
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
        self.speed = speed
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
        """
        1. get the sketch_edge_definer result from `self.img_path`
        2. setup the screen to prepare the drawing
        3. for each line:
            1. for each pixel on the line
                a. draw the pixel
        4. hide turtles
        """
        img = self.sketch_edge_definer()
        width = img.shape[1]
        height = img.shape[0]

        self.screen.title("Zhang Gui")
        self.screen.screensize(width, height)
        self.screen.tracer(self.speed)

        for ypos in range(int(height / 2), int(height / -2), -1):
            self.drawer.penup()
            self.drawer.goto(-(width / 2), ypos)

            self.drawer.pendown()
            for xpos in range(-int(width / 2), int(width / 2), 1):
                pix_width = int(xpos + (width / 2))
                pix_height = int(height / 2 - ypos)
                drawer_color = self.rgb_to_hex(
                    img[pix_height, pix_width],
                    img[pix_height, pix_width],
                    img[pix_height, pix_width],
                )
                self.drawer.color(drawer_color)
                self.drawer.forward(1)
            self.screen.update()
            self.drawer.hideturtle()
        self.drawer.hideturtle()

        done()


def main():
    try:
        if len(argv) > 3 and int(argv[3]) in range(11):
            drawer = ImgDrawer(argv[1], argv[2], argv[3])
            drawer.sketch_edge_definer()
            drawer.sketch_drawer()
        else:
            raise Exception("")
    except:
        print(
            "Please specify a valid image path, a valid odd kernel size and a speed between 0 and 10."
        )


if __name__ == "__main__":
    main()
