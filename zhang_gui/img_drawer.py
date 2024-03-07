# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

from sys import argv
from turtle import Screen, Turtle, done, speed, color

from cv2 import (
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    GaussianBlur,
    bitwise_not,
    cvtColor,
    divide,
    imread,
)


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 01
    Goal: Draw a sketch
    """

    k_size: int
    screen: Screen
    drawer: Turtle

    def __init__(self, img_path: str, k_size: int | str, _speed: int | str = 5):
        self.k_size = int(k_size)
        self.image = imread(img_path)
        speed(int(_speed))

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

    def img_transformer(self) -> None:
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
        grey_img = cvtColor(self.image, COLOR_BGR2GRAY)
        inverted_img = bitwise_not(grey_img)
        blurred_img = GaussianBlur(inverted_img, (self.k_size, self.k_size), 0)
        inverted_blurred_img = bitwise_not(blurred_img)

        return (grey_img, inverted_blurred_img)

    def sketch_edge_definer(self) -> None:
        grey_img, inverted_blurred_img = self.img_transformer()
        self.image = divide(grey_img, inverted_blurred_img, scale=256.0)

    def sketch_drawer(self) -> any:
        img = self.image
        width = img.shape[1]
        height = img.shape[0]

        self.screen = Screen()
        self.screen.screensize(width, height)
        self.drawer = Turtle()
        self.screen.tracer(0)

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
                color("white")
                self.drawer.forward(1)
            self.screen.update()
            self.drawer.hideturtle()
        self.drawer.hideturtle()

        done()


def main():
    try:
        if len(argv) > 3:
            drawer = ImgDrawer(argv[1], argv[2], argv[3])
            drawer.sketch_edge_definer()
            drawer.sketch_drawer()
        else:
            raise Exception("""Please specify an image path and a kernel size.""")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
