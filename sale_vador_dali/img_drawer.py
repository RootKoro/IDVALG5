# Author: Cyr Mathieu GUEYE, Maïssane QASMI, Dona DOSSA, Hacene SADOUDI# Author: Cyr Mathieu GUEYE
# Licenceless
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software

from sys import argv

from cv2 import (
    COLOR_BGR2GRAY,
    GaussianBlur,
    bitwise_not,
    cvtColor,
    destroyAllWindows,
    divide,
    imread,
    imshow,
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

    def __init__(self, img_path: str, k_size: int):
        self.img_path = img_path
        self.k_size = k_size

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

    def sketch_edge_drawer(self):
        grey_img, inverted_blurred_img = self.img_transformer()
        sketch_img = divide(grey_img, inverted_blurred_img, scale=256.0)

        # Save Sketch
        # cv2.imwrite("sketch.png", sketch_img)

        # Display sketch
        imshow("sketch image", sketch_img)
        waitKey(0)
        destroyAllWindows()


def main():
    try:
        if len(argv) > 2:
            bfl = ImgDrawer(argv[1], int(argv[2]))
            bfl.sketch_edge_drawer()
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
