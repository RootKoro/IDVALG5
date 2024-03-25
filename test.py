from argparse import ArgumentParser
from os.path import exists
from turtle import Screen, Turtle, done

from _tkinter import TclError
from blurgenerator import lens_blur
from cv2 import (
    COLOR_BGR2RGB,
    Canny,
    cvtColor,
    GaussianBlur,
    bilateralFilter,
    bitwise_not,
    boxFilter,
    imread,
    imshow,
    medianBlur,
)
from numpy import Infinity, int_, median
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree


def rgb_to_hex(r: int, g: int, b: int) -> None:
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


img = imread("assets/lion.jpg")
img = cvtColor(img, COLOR_BGR2RGB)
img = img.reshape((img.shape[1] * img.shape[0], 3))

kmeans = KMeans(n_init=10)
_ = kmeans.fit(img)
centroid = kmeans.cluster_centers_

colors = list(map(lambda x: (int(x[0]), int(x[1]), int(x[2])), centroid))
colors = list(map(lambda x: rgb_to_hex(x[0], x[1], x[2]), colors))

print(colors)
