# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI
# Licenceless

from _tkinter import TclError
from argparse import ArgumentParser
from numpy import median
from os.path import exists
from turtle import Screen, Turtle, done

from blurgenerator import lens_blur
from cv2 import (
    GaussianBlur,
    Canny,
    bilateralFilter,
    bitwise_not,
    boxFilter,
    imread,
    medianBlur,
)

BLURS = ("bilateral", "gaussian", "lens", "linear", "median", "none", "default")


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 03
    Goal: Draw an animated sketch
    """

    blur_type: str
    k_size: int
    speed: int
    drawer: Turtle
    screen: Screen

    def __init__(self, blur: str, k_size: int | str, speed: int | str = 5):
        self.blur_type = blur
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

    def image_blurer(self, image: any) -> any:
        """
        From the image object:
            - check the user choice
            - return the corresponding blurred image
        """
        if self.blur_type == "bilateral":
            return bilateralFilter(image, self.ksize, 75, 75)
        elif self.blur_type == "gaussian":
            return GaussianBlur(image, (self.ksize, self.ksize), 0)
        elif self.blur_type == "lens":
            return lens_blur(image, self.ksize)
        elif self.blur_type == "linear":
            return boxFilter(image, -1, (self.ksize, self.ksize))
        elif self.blur_type == "median":
            return medianBlur(image, self.ksize)
        elif self.blur_type == "default":
            return GaussianBlur(image, (3, 3), 0)
        else:
            return image

    def sketch_edge_definer(self, image: any) -> any:
        """
        1- Read the image
        2- get the blured image
        3- Get the median value of the img
            The image is converted into a 2 dimensional array of bits
            the median is retrieved from that array
        4- draw a new 2 dimensional array of bits containing the points
        retreived from the calculation of Canny algorithm
        5- return the new img corresponding to the new array
        """
        blured = self.image_blurer(image)
        median_value = median(blured)
        return bitwise_not(Canny(blured, median_value, 255))

    def sketch_drawer(self, img_path) -> any:
        """
        1. get the sketch_edge_definer result from `self.img_path`
        2. setup the screen to prepare the drawing
        3. for each line:
            1. for each pixel on the line
                a. draw the pixel
        4. hide turtles
        """
        image = imread(img_path)
        sketch_edge = self.sketch_edge_definer(image)
        width = sketch_edge.shape[1]
        height = sketch_edge.shape[0]

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
                    sketch_edge[pix_height, pix_width],
                    sketch_edge[pix_height, pix_width],
                    sketch_edge[pix_height, pix_width],
                )
                self.drawer.color(drawer_color)
                self.drawer.forward(1)
            self.screen.update()
            self.drawer.hideturtle()
        self.drawer.hideturtle()

        done()


def help_menu():
    print("Usage:")
    print("img_drawer.py [-h/--help]")
    print(
        "img_drawer.py -i/--image path/to/image -b/--blur blur_type [-k/--kernel kernel] [-s/--speed speed]"
    )
    print(
        "`blur_type` in : default, bilateral, gaussian, lens, linear, median and none (for no blur)"
    )
    print("`kernel` : an integer greater than 0")
    print("`speed`: the spped of the speed of the drawing")
    print("\nNote:")
    print("for default and none (blur) you don't need to specify any kernel")
    print("for gaussian and median (blur) the kernel value must be odd")
    print("\nex. img_drawer.py -i lion.png -b gaussian -k 3 -s 1")


try:
    args = ArgumentParser()
    args.add_argument("-i", "--image", required=True, help="image path")
    args.add_argument(
        "-b",
        "--blur",
        required=True,
        help="blur type : bilateral, gaussian, lens, linear, median and none (for no blur)",
    )
    args.add_argument("-k", "--kernel", required=False, help="kernel size")
    args.add_argument("-s", "--speed", required=False, help="speed of the turtle")
    args = vars(args.parse_args())

    if not exists(args["image"]):
        print("error: File does not exist !")
        exit(1)
    if args["blur"] not in BLURS:
        print(f"error: Your choice must be in {BLURS} !")
        exit(1)
    if args["blur"] not in ("none", "default") and args["kernel"] == None:
        print("error: this blur type needs a kernel size (blur level) !")
        exit(1)
    if args["blur"] not in ("none", "default") and int(args["kernel"]) < 1:
        print("error: The kernel size must be greater than 1 !")
        exit(1)
    if args["blur"] in ("gaussian", "median") and int(args["kernel"]) % 2 == 0:
        print("error: For the gaussian or median blur, the kernel value must be odd !")
        exit(1)

    blur = args["blur"]
    kernel = args["kernel"] if args["kernel"] else 0
    svd = ImgDrawer(
        args["blur"],
        int(args["kernel"]) if args["kernel"] else 0,
        int(args["speed"]) if args["speed"] else 0,
    )
    svd.sketch_drawer(args["image"])
except TclError:
    print("Forced closing of sketch!")
except TypeError:
    print("error: Unsupported type of file given !")
except Exception:
    help_menu()
