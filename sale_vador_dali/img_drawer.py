# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA
# Licenceless

from argparse import ArgumentParser
from numpy import median
from os.path import exists

from blurgenerator import lens_blur
from cv2 import (
    GaussianBlur,
    Canny,
    bilateralFilter,
    bitwise_not,
    boxFilter,
    destroyAllWindows,
    imread,
    imshow,
    medianBlur,
    waitKey,
)

CMD = ("-b", "-i", "-k", "--blur", "--image", "--kernel")
BLURS = ("bilateral", "gaussian", "lens", "linear", "median", "none", "default")


class ImgDrawer:
    """
    Module: IDV-ALGO5
    Step: 02
    Goal: Draw a sketch
    """

    blur_type: str
    ksize: int

    def __init__(self, blur_type: str, ksize: int) -> None:
        self.blur_type = blur_type
        self.ksize = ksize

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

    def sketch_edge_drawer(self, img_path: str) -> None:
        """
        - Read the image
        - Get the blured image
        - Get the median value of the img
            The image is converted into a 2 dimensional array of bits
            the median is retrieved from that array
        - draw a new 2 dimensional array of bits containing the points
        retreived from the calculation of Canny algorithm
        - Show the new img corresponding to the new array
        """
        blured = self.image_blurer(imread(img_path))
        median_value = median(blured)
        sketch_img = bitwise_not(Canny(blured, median_value, 255))

        imshow("sketch image", sketch_img)
        waitKey(0)
        destroyAllWindows()


def help_menu():
    print("Usage:")
    print("img_drawer.py [-h|--help]")
    print(
        "img_drawer.py [-i|--image] path/to/image [-b|--blur] blur_type [-k|--kernel] kernel"
    )
    print(
        "`blur_type` in : bilateral, gaussian, lens, linear, median and none (for no blur)"
    )
    print("`kernel` : an integer greater than 0")
    print("ex. img_drawer.py -i lion.png -b gaussian -k 3")


def is_valid(cmd: str) -> bool:
    """ """
    global CMD
    return True if cmd in CMD else False


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

    svd = ImgDrawer(args["blur"], int(args.get("kernel", -1)))
    svd.sketch_edge_drawer(args["image"])
except TypeError:
    print("error: Unsupported type of file given !")
except Exception:
    help_menu()
