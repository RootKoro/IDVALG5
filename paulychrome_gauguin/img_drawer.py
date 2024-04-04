# Author: Maïssane QASMI, Dona DOSSA, Cyr Mathieu GUEYE
# Licenceless

from argparse import ArgumentParser
from os.path import exists
from turtle import Screen, Turtle, done

from _tkinter import TclError
from cv2 import COLOR_BGR2RGB, Canny, GaussianBlur, bitwise_not, cvtColor, imread
from numpy import median
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree


class Utils:

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

    def __init__(
        self,
        img_path: str,
        speed: int,
    ):
        self.img_path = img_path

        self.image2D = imread(img_path, 2)
        self.image3D = imread(img_path)
        self.height, self.width = self.image2D.shape

        self.screen = Screen()
        self.screen.screensize(self.width, self.height)
        self.screen.title("Paulychrome Gaugin")
        self.screen.tracer(speed)

        self.drawer = Turtle()
        self.drawer.hideturtle()
        self.drawer.penup()
        self.drawer.speed(speed)

        self.utils = Utils()

    def get_pixel_coords(self, image: any, rgb: tuple | None = None) -> list:
        """
        If RGB is not provided, returns the coordinates of none white pixels
        If RGB is provided, returns the coordinates of pixels of that color
        """
        coords = []
        height = len(image)
        for y, row in enumerate(image):
            for x, value in enumerate(row):
                if (not rgb and value <= 127) or (
                    rgb
                    and value[0] == rgb[0]
                    and value[1] == rgb[1]
                    and value[2] == rgb[2]
                ):
                    coords.append([x, height - y])
        return coords

    def get_pixel_color(self, pixel_rgb: tuple) -> tuple:
        """
        Calculate the difference between the pixel's color and the palette's colors
        and returns the palette's color that provides the least difference.
        """
        diffs = []
        for palette_color in self.palette:
            diff = 0
            for i, val in enumerate(pixel_rgb):
                diff += abs(palette_color[i] - val)
            diffs.append(diff)
        tiniest_diff_index = diffs.index(min(diffs))
        return self.palette[tiniest_diff_index]

    def classify_pixels(self, image: any) -> any:
        """
        Changes each pixel's color into the the it's closest from the palette
        """
        for row_id, row in enumerate(image):
            for i, pixel in enumerate(row):
                image[row_id][i] = self.get_pixel_color(pixel)
        return image

    def get_cluster_colors(self, image: any) -> any:
        """
        Get a palette of dominant colors from the given image.
        1. convert the image from BRG to RGB format
        2. reshape it so it can be passed to a clustering algorithm
        3. initialize the KMeans object that will perform k-means clustering algorithm
        4. Compute the k-means clustering algorithm
        5. Get the clusters centers
        6. Convert them into a list of RGB colors
        7. Returns the RGB color list
        """
        image = cvtColor(image, COLOR_BGR2RGB)
        switched = image.reshape((image.shape[1] * image.shape[0], 3))
        kmeans = KMeans(n_clusters=20, n_init=10)
        _ = kmeans.fit(switched)
        centroid = kmeans.cluster_centers_
        colors = list(map(lambda x: (int(x[0]), int(x[1]), int(x[2])), centroid))
        return colors

    def blur_image(self, image: any) -> any:
        return GaussianBlur(image, (3, 3), 0)

    def define_sketch_edge(self, image: any) -> any:
        """
        Defines the sketch of an image
        1. calculates the median value of the pixels
        2. detects the edges of the image using the Canny edge algorithm
        3. inverse the new image obtained with the Canny edge algorithm
        4. returns the inversed image
        """
        median_value = median(image)
        return bitwise_not(Canny(image, median_value, 255))

    def draw(self, coords: list) -> None:
        """
        Draws each pixel from it's coordinates in the `coords` list
        while using a k-dimensional tree to place the coordinates,
        helping to get the nearest pixel to represent after
        drawing each pixel (NNS).
        """
        tree = KDTree(coords)
        current = 0
        explored_ind = [0]

        while len(coords) > 1:
            self.drawer.goto(
                coords[current][0] - (self.width / 2),
                coords[current][1] - (self.height / 2),
            )
            ind = tree.query_radius([coords[current]], r=1.42)
            ind = ind[0].tolist()
            ind = [value for value in ind if value not in explored_ind]

            if len(ind) >= 1:
                self.drawer.pendown()
                self.drawer.goto(
                    coords[ind[0]][0] - (self.width / 2),
                    coords[ind[0]][1] - (self.height / 2),
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

    def theArtist(self) -> None:
        """
        Draws the sketch of `self.image` and paints it artistically.
        """
        blured = self.blur_image(self.image2D)
        sketch = self.define_sketch_edge(blured)
        sketch_coords = self.get_pixel_coords(sketch)
        self.draw(sketch_coords)

        self.palette = self.get_cluster_colors(self.image3D)

        image_art = self.classify_pixels(self.image3D)
        for color in self.palette:
            pixel_coords = self.get_pixel_coords(image_art, color)
            if len(pixel_coords) > 0:
                pixel_color = self.utils.rgb_to_hex(
                    int(color[0]),
                    int(color[1]),
                    int(color[2]),
                )
                self.drawer.color(pixel_color)
                self.draw(pixel_coords)

        done()


def help_menu():
    command = "img_drawer.py"
    image = "-i|--image path/to/image"
    speed = "-s|--speed speed"
    print("Usage:")
    print("img_drawer.py [-h|--help]")
    print(f"{command} {image} [{speed}]")
    print("\nex. img_drawer.py -i lion.png -s 1")


try:
    args = ArgumentParser()
    args.add_argument("-i", "--image", required=True, help="image path")
    args.add_argument("-s", "--speed", required=False, help="speed of the turtle")
    args = vars(args.parse_args())

    if not exists(args["image"]):
        print("error: File does not exist !")
        exit(1)
    try:
        if args["speed"] and int(args["speed"]) not in range(11):
            print("warning: The speed value should be within [0, 10]")
            print("warning: Other values will be replaced with 10 !")
            speed = 10
        else:
            speed = int(args["speed"])
    except Exception:
        print("error: The speed vlaue must be a number")
        exit(1)

    img_drawer = ImgDrawer(args["image"], speed)
    img_drawer.theArtist()
except TclError:
    print("Forced closing of sketch!")
except TypeError:
    print("error: Unsupported type of file given !")
except Exception as e:
    print(e)
    help_menu()
