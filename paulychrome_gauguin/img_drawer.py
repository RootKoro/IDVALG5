# Author: Maïssane QASMI, Dona DOSSA, Cyr Mathieu GUEYE
# Licenceless

from _tkinter import TclError
from argparse import ArgumentParser
from numpy import median, Infinity
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
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree

BLURS = ("bilateral", "gaussian", "lens", "linear", "median", "none", "default")
COLORS = ("classification", "clustering")
SAVANE_PALETTE = [
    (35, 30, 24),
    (136, 72, 37),
    (210, 152, 106),
    (223, 201, 203),
    (180, 173, 31),
]


class Utils:
    """ """

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


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 05
    Goal: Draw the sketch of an image and paint it
    """

    coloring: str
    blur_type: str
    ksize: int
    speed: int
    palette: list[tuple[int]]
    drawer: Turtle
    screen: Screen
    utils: Utils

    def __init__(
        self,
        blur_type: str,
        coloring: str,
        ksize: int | str,
        speed: int | str,
        palette: list[tuple],
    ):
        self.coloring = coloring
        self.blur_type = blur_type
        self.ksize = int(ksize)
        self.palette = palette
        self.speed = int(speed)

        self.screen = Screen()
        self.screen.title("Renoir Blanc")
        self.screen.tracer(self.speed)

        self.drawer = Turtle()
        self.drawer.hideturtle()
        self.drawer.penup()

        self.utils = Utils()

    def get_pixel_coords(self, image: any, rgb: tuple | None = None) -> list:
        """ """
        coords = []
        height = len(image)
        for y, row in enumerate(image):
            for x, value in enumerate(row):
                if not rgb and value <= 127:
                    coords.append([x, height - y])
                if (
                    rgb
                    and value[0] == rgb[0]
                    and value[1] == rgb[1]
                    and value[2] == rgb[2]
                ):
                    coords.append([x, height - y])
        return coords

    def get_pixel_color(self, pixel_rgb: tuple) -> tuple:
        """ """
        diffs = []
        for palette_color in self.palette:
            diff = 0
            for i, val in enumerate(pixel_rgb):
                diff += abs(palette_color[i] - val)
            diffs.append(diff)
        tiniest_diff_index = diffs.index(min(diffs))
        return self.palette[tiniest_diff_index]

    def pixel_classifier(self, image: any) -> any:
        """ """
        for row in image:
            for i, pixel in enumerate(row):
                row[i] = self.get_pixel_color(pixel)
        return image

    def pixel_clusterer(self, image: any) -> any:
        """ """
        height, width, dimensions = image.shape
        switched = image.reshape((height * width, dimensions))
        kmeans = KMeans().fit(switched)
        return kmeans

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

    def painter(self, width: int, height: int, coords: list, color: str) -> None:
        """ """
        self.drawer.color(color)
        self.drawer.penup()
        for coord in coords:
            self.drawer.setpos(coord[0] - (width / 2), coord[1] - (height / 2))
            self.drawer.dot(1)

    def draw(self, img_path: str) -> None:
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
        self.screen.screensize(width, height)

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

    def finisher(self, img_path) -> None:
        """ """
        image = imread(img_path)
        if self.coloring == "classification":
            image = self.pixel_classifier(image)
            height, width, _ = image.shape
            for color in self.palette:
                color_coords = self.get_pixel_coords(image, color)
                hex_color = self.utils.rgb_to_hex(
                    int(color[0]),
                    int(color[1]),
                    int(color[2]),
                )

                self.painter(width, height, color_coords, hex_color)
        else:
            kmeans = self.pixel_clusterer(image)
            height, width, _ = image.shape
            mapping = kmeans.labels_.reshape((height, width))
            ngroup = len(kmeans.cluster_centers_)
            for i in range(ngroup):
                color = kmeans.cluster_centers_[i]
                color = self.utils.rgb_to_hex(
                    int(color[0]),
                    int(color[1]),
                    int(color[2]),
                )
                coords = self.get_pixel_coords(mapping, i)
                self.painter(width, height, coords, color)
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


# try:
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
args.add_argument("-c", "--coloring", required=True, help="coloring algorithm")
args = vars(args.parse_args())

if not exists(args["image"]):
    print("error: File does not exist !")
    exit(1)
if args["blur"] not in BLURS:
    print(f"error: Blur choice must be in {BLURS} !")
    exit(1)
if args["blur"] not in ("none", "default") and args["kernel"] == None:
    print("error: This blur type needs a kernel size (blur level) !")
    exit(1)
if args["blur"] not in ("none", "default") and int(args["kernel"]) < 1:
    print("error: The kernel size must be greater than 1 !")
    exit(1)
if args["blur"] in ("gaussian", "median") and int(args["kernel"]) % 2 == 0:
    print("error: For the gaussian or median blur, the kernel value must be odd !")
    exit(1)
if args["speed"] and int(args["speed"]) not in range(11):
    print(
        "warning: Speed should be within [0, 10], other values are considerated as 10"
    )
if args["coloring"] not in COLORS:
    print(f"error: Coloring choice must be one of the following: {COLORS}")
if not exists(args["image"]):
    print("error: File does not exist !")
    exit(1)
if args["blur"] not in BLURS:
    print(f"error: Blur choice must be in {BLURS} !")
    exit(1)
if args["blur"] not in ("none", "default") and args["kernel"] == None:
    print("error: This blur type needs a kernel size (blur level) !")
    exit(1)
if args["blur"] not in ("none", "default") and int(args["kernel"]) < 1:
    print("error: The kernel size must be greater than 1 !")
    exit(1)
if args["blur"] in ("gaussian", "median") and int(args["kernel"]) % 2 == 0:
    print("error: For the gaussian or median blur, the kernel value must be odd !")
    exit(1)
if args["speed"] and int(args["speed"]) not in range(11):
    print(
        "warning: Speed should be within [0, 10], other values are considerated as 10"
    )
if args["coloring"] not in COLORS:
    print(f"error: Coloring choice must be one of the following: {COLORS}")

svd = ImgDrawer(
    args["blur"],
    args["coloring"],
    int(args["kernel"]) if args["kernel"] else 0,
    int(args["speed"]) if args["speed"] else 0,
    SAVANE_PALETTE,
)
svd.draw(args["image"])
svd.finisher(args["image"])
# except TclError:
#     print("Forced closing of sketch!")
# except TypeError:
#     print("error: Unsupported type of file given !")
# except Exception as e:
#     print(e)
#     help_menu()
