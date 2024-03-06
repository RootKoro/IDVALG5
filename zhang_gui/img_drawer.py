# Author: Cyr Mathieu GUEYE
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

from sys import argv
from turtle import Screen, Turtle, done, speed

from cv2 import (
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    GaussianBlur,
    bitwise_not,
    cvtColor,
    destroyAllWindows,
    divide,
    imread,
    imshow,
    threshold,
    waitKey,
)


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

    def img_transformer(self) -> tuple:
        """
        1- Convert the image to grey
        2- Invert the converted image
        3- Blur the inverted image
        4- invert the blurred image

        Params:
        -------
            img_path : string
                path to the image
            k_size : int
                kernel size ; which might defer depending on the image ;
                on small images, the kernel size should be very small
                and for large images, the kernel size should be very large
        """
        img = imread(self.img_path)
        grey_img = cvtColor(img, COLOR_BGR2GRAY)
        inverted_img = bitwise_not(grey_img)
        blurred_img = GaussianBlur(inverted_img, (self.k_size, self.k_size), 0)
        inverted_blurred_img = bitwise_not(blurred_img)

        return (grey_img, inverted_blurred_img)

    def sketch_edge_definer(self) -> any:
        grey_img, inverted_blurred_img = self.img_transformer()
        return divide(grey_img, inverted_blurred_img, scale=256.0)

    def sketch_drawer(self) -> any:
        speed(self.speed)
        img = self.sketch_edge_definer()
        ret, binary_img = threshold(img, 127, 255, THRESH_BINARY)
        width = img.shape[1]
        height = img.shape[0]

        self.screen = Screen()
        self.screen.screensize(width, height)
        self.drawer = Turtle()
        self.screen.tracer(0)

        for x_pos in range(int(height / 2), int(height / -2), -1):
            self.drawer.penup()
            self.drawer.goto(-(width / 2), x_pos)

            for y_pos in range(-int(width / 2), int(width / 2), 1):
                pix_width = int(y_pos + (width / 2))
                pix_height = int(height / 2 - x_pos)
                if binary_img[pix_height, pix_width] == 0:
                    self.drawer.pendown()
                    self.drawer.forward(1)
                else:
                    self.drawer.penup()
                    self.drawer.forward(1)
            self.screen.update()

        self.drawer.hideturtle()

        done()


def main():
    try:
        if len(argv) > 3:
            drawer = ImgDrawer(argv[1], argv[2], argv[3])
            drawer.sketch_drawer()
        else:
            raise Exception("""Please specify an image path and a kernel size.""")
    except Exception as e:
        print(e)
        print(
            """
Retry while checking the following steps:
    the first argument is a valid image path
    the second argument is an integer
    The integer given as second argument should be proportional o the image

ex. big_fernand_leger.py assets/img.png 5
            """
        )


if __name__ == "__main__":
    main()
