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
from sklearn.neighbors import KDTree

BLURS = ("bilateral", "gaussian", "lens", "linear", "median", "none", "default")


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 04
    Goal: Draw an animated sketch
    """

    blur_type: str
    ksize: int
    speed: int
    drawer: Turtle
    screen: Screen

    def __init__(self, blur_type: str, ksize: int | str, speed: int | str = 5):
        self.blur_type = blur_type
        self.ksize = int(ksize)
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

    def get_pixel_coords(self, image: any) -> list:
        """
        retrieves and returns non-white pixels' coordinates
        1- for each list (line) and it's index in the main list (image)
        2- for each pixel and it's index in the line
        3- append the pixel's indexes (coordinates) in the `coords` list
        4- return the `coords` list after proccessing all pixels of the image
        """
        coords = []
        height = len(image)
        for y, line in enumerate(image):
            for x, value in enumerate(line):
                if value <= 127:
                    coords.append([x, height - y])
        return coords

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
        1- Get the blured image
        2- Get the median value of the image
            The image is converted into a 2 dimensional array of bits
            from which the median value is retreived
        3- draw a new 2 dimensional array of bits containing the points
        retreived from the calculation of Canny algorithm
        4- return the new img corresponding to the new array
        """
        blured = self.image_blurer(image)
        median_value = median(blured)
        return bitwise_not(Canny(blured, median_value, 255))

    def sketch_drawer(self, img_path: str) -> any:
        """
        1. get the sketch of the image
        2. get non-white pixels' coordinates
        3. initialize a KDTree
        4. get the shape of the image
        5. set up the screen and the drawer
        6. drawing of each pixel following the algorithm of `Nearest neighbour search`
        """
        image = imread(img_path, 2)
        image = self.sketch_edge_definer(image)
        coords = self.get_pixel_coords(image)
        tree = KDTree(coords)
        width = image.shape[1]
        height = image.shape[0]
        current = 0
        explored_ind = [0]

        self.screen.title("Renoir Blanc")
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
        done()


def help_menu():
    print("Usage:")
    print("img_drawer.py [-h|--help]")
    print(
        "img_drawer.py -i|--image path/to/image -b|--blur blur_type [-k|--kernel kernel] [-s|--speed speed]"
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
