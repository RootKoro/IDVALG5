# Author: Maïssane QASMI, Dona DOSSA, Cyr Mathieu GUEYE
# Licenceless

from argparse import ArgumentParser
from os.path import exists
from turtle import Screen, Turtle, done

from _tkinter import TclError
from blurgenerator import lens_blur
from cv2 import (
    COLOR_BGR2RGB,
    Canny,
    GaussianBlur,
    bilateralFilter,
    bitwise_not,
    boxFilter,
    cvtColor,
    imread,
    imshow,
    medianBlur,
)
from numpy import Infinity, int_, median
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

screen: Screen = Screen()
screen.title("Paulychrome Gaugin")

drawer: Turtle = Turtle()
drawer.hideturtle()
drawer.penup()


def rgb_to_hex(r: int, g: int, b: int) -> None:
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


def get_pixel_coords(image: any, rgb: tuple | None = None) -> list:
    """ """
    coords = []
    height = len(image)
    for y, row in enumerate(image):
        for x, value in enumerate(row):
            if not rgb and value <= 127:
                coords.append([x, height - y])
            if rgb and value[0] == rgb[0] and value[1] == rgb[1] and value[2] == rgb[2]:
                coords.append([x, height - y])
    return coords


def get_pixel_color(pixel_rgb: tuple, palette: list) -> tuple:
    """ """
    diffs = []
    for palette_color in palette:
        diff = 0
        for i, val in enumerate(pixel_rgb):
            diff += abs(palette_color[i] - val)
        diffs.append(diff)
    tiniest_diff_index = diffs.index(min(diffs))
    return palette[tiniest_diff_index]


def pixel_classifier(image: any, palette: list) -> any:
    """ """
    for row_id, row in enumerate(image):
        for i, pixel in enumerate(row):
            image[row_id][i] = get_pixel_color(pixel, palette)
    return image


def get_cluster_colors(image: any) -> any:
    """ """
    image = cvtColor(image, COLOR_BGR2RGB)
    switched = image.reshape((image.shape[1] * image.shape[0], 2))
    kmeans = KMeans(n_clusters=5, n_init=10)
    _ = kmeans.fit(image)
    centroid = kmeans.cluster_centers_
    colors = list(map(lambda x: (int(x[0]), int(x[1]), int(x[2])), centroid))
    return colors


def image_blurer(image: any, blur_type: str) -> any:
    """
    From the image object:
        - check the user choice
        - return the corresponding blurred image
    """
    if blur_type == "bilateral":
        return bilateralFilter(image, ksize, 75, 75)
    elif blur_type == "gaussian":
        return GaussianBlur(image, (ksize, ksize), 0)
    elif blur_type == "lens":
        return lens_blur(image, ksize)
    elif blur_type == "linear":
        return boxFilter(image, -1, (ksize, ksize))
    elif blur_type == "median":
        return medianBlur(image, ksize)
    elif blur_type == "default":
        return GaussianBlur(image, (3, 3), 0)
    else:
        return image


def sketch_edge_definer(image: any) -> any:
    """
    1- Get the blured image
    2- Get the median value of the image
        The image is converted into a 2 dimensional array of bits
        from which the median value is retreived
    3- draw a new 2 dimensional array of bits containing the points
    retreived from the calculation of Canny algorithm
    4- return the new img corresponding to the new array
    """
    median_value = median(image)
    return bitwise_not(Canny(image, median_value, 255))


def painter(width: int, height: int, coords: list, color: str, drawer: Turtle) -> None:
    """ """
    drawer.color(color)
    drawer.penup()
    for coord in coords:
        drawer.setpos(coord[0] - (width / 2), coord[1] - (height / 2))
        drawer.dot(1)


def draw(coords: list, height: int, width: int, drawer: Turtle) -> None:
    """
    1. get the sketch of the image
    2. get non-white pixels' coordinates
    3. initialize a KDTree
    4. get the shape of the image
    5. set up the screen and the drawer
    6. drawing of each pixel following the algorithm of `Nearest neighbour search`
    """
    tree = KDTree(coords)
    current = 0
    explored_ind = [0]

    while len(coords) > 1:
        drawer.goto(coords[current][0] - (width / 2), coords[current][1] - (height / 2))
        ind = tree.query_radius([coords[current]], r=1.42)
        ind = ind[0].tolist()
        ind = [value for value in ind if value not in explored_ind]

        if len(ind) >= 1:
            drawer.pendown()
            drawer.goto(
                coords[ind[0]][0] - (width / 2), coords[ind[0]][1] - (height / 2)
            )
            drawer.penup()
            explored_ind.append(ind[0])
            current = ind[0]

        else:
            tmp = coords[current]
            coords = [coords[i] for i in range(0, len(coords)) if i not in explored_ind]
            explored_ind = []
            if len(coords) > 1:
                tree = KDTree(coords)
                _, i = tree.query([tmp], k=2)
                i = i.flatten()
                current = i[1]


# def finisher(image: any, coloring_model: str, drawer: Turtle, palette: list) -> None:
#     """ """
#     height, width, _ = image.shape
#     if coloring_model == "classification":
#         image = pixel_classifier(image, palette)
#         for color in palette:
#             color_coords = get_pixel_coords(image, color)
#             hex_color = rgb_to_hex(
#                 int(color[0]),
#                 int(color[1]),
#                 int(color[2]),
#             )
#             painter(width, height, color_coords, hex_color, drawer)
#     else:
#         kmeans = pixel_clusterer(image)
#         mapping = kmeans.labels_.reshape((height, width))
#         ngroup = len(kmeans.cluster_centers_)
#         for i in range(ngroup):
#             color = kmeans.cluster_centers_[i]
#             color = rgb_to_hex(
#                 int(color[0]),
#                 int(color[1]),
#                 int(color[2]),
#             )
#             coords = get_pixel_coords(mapping, i)
#             painter(width, height, coords, color, drawer)


# def artist(
#     image2D: any,
#     image3D: any,
#     drawer: Turtle,
#     coloring_model: str,
#     palette: list,
# ) -> None:
#     """ """
#     height, width = image2D.shape
#     coords = get_pixel_coords(image2D)
#     tree = KDTree(coords)
#     current = 0
#     explored_ind = [0]

#     while len(coords) > 1:
#         drawer.goto(coords[current][0] - (width / 2), coords[current][1] - (height / 2))
#         ind = tree.query_radius([coords[current]], r=1.42)
#         ind = ind[0].tolist()
#         ind = [value for value in ind if value not in explored_ind]

#         if len(ind) >= 1:
#             drawer.pendown()
#             drawer.goto(
#                 coords[ind[0]][0] - (width / 2), coords[ind[0]][1] - (height / 2)
#             )
#             drawer.penup()
#             explored_ind.append(ind[0])
#             current = ind[0]

#         else:
#             tmp = coords[current]
#             coords = [coords[i] for i in range(0, len(coords)) if i not in explored_ind]
#             explored_ind = []
#             if len(coords) > 1:
#                 tree = KDTree(coords)
#                 _, i = tree.query([tmp], k=2)
#                 i = i.flatten()
#                 current = i[1]

#     height, width, _ = image3D.shape
#     current = 0
#     explored_ind = [0]
#     if coloring_model == "classification":
#         image = pixel_classifier(image3D, palette)
#         for color in palette:
#             print(color)
#             color_coords = get_pixel_coords(image, color)
#             if not color_coords:
#                 continue
#             print("color found!")
#             hex_color = rgb_to_hex(
#                 int(color[0]),
#                 int(color[1]),
#                 int(color[2]),
#             )
#             drawer.color(hex_color)
#             # for coord in color_coords:
#             #     drawer.setpos(coord[0] - (width / 2), coord[1] - (height / 2))
#             #     drawer.pendown()
#             #     drawer.dot(1)
#             #     drawer.penup()
#         painter(width, height, color_coords, hex_color, drawer)
#     else:
#         kmeans = pixel_clusterer(image)
#         mapping = kmeans.labels_.reshape((height, width))
#         ngroup = len(kmeans.cluster_centers_)
#         for i in range(ngroup):
#             color = kmeans.cluster_centers_[i]
#             color = rgb_to_hex(
#                 int(color[0]),
#                 int(color[1]),
#                 int(color[2]),
#             )
#             coords = get_pixel_coords(mapping, i)
#             painter(width, height, coords, color, drawer)


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
args.add_argument("-m", "--model", required=True, help="coloring algorithm")
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
if args["model"] not in COLORS:
    print(f"error: Coloring choice must be one of the following: {COLORS}")


image3D = imread(args["image"])
image2D = imread(args["image"], 2)
blur_type = args["blur"]
ksize = int(args["kernel"]) if args["kernel"] else None
speed = int(args["speed"]) if args["speed"] else 0
speed = speed if speed in range(11) else 10
model = args["model"]
height, width = image2D.shape

screen.tracer(speed)
screen.screensize(width, height)

# 2D sketch drawing
blured = image_blurer(image2D, blur_type)
sketch = sketch_edge_definer(blured)
sketch_coords = get_pixel_coords(sketch)
draw(sketch_coords, height, width, drawer)
if model == "classification":
    image_art = pixel_classifier(image3D, SAVANE_PALETTE)
    palette = SAVANE_PALETTE
else:
    image_art = image3D
    palette = get_cluster_colors(image3D)

for color in palette:
    pixel_coords = get_pixel_coords(image_art, color)
    if len(pixel_coords) > 0:
        pixel_color = rgb_to_hex(int(color[0]), int(color[1]), int(color[2]))
        drawer.color(pixel_color)
        draw(pixel_coords, height, width, drawer)


done()

# svd = ImgDrawer(
#     args["blur"],
#     args["coloring"],
#     int(args["kernel"]) if args["kernel"] else 0,
#     int(args["speed"]) if args["speed"] else 0,
#     SAVANE_PALETTE,
# )
# svd.draw(args["image"])
# svd.finisher(args["image"])s
# except TclError:
#     print("Forced closing of sketch!")
# except TypeError:
#     print("error: file type or another value in the parameters must have the wrong type!")
# except Exception as e:
#     print(e)
#     help_menu()
