import cv2
import turtle


def test():
    # Binary Image

    img = cv2.imread("assets/tree-night.jpg")
    ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    width = int(img.shape[1])
    height = int(img.shape[0])

    # Turtle Setup

    my_screen = turtle.Screen()
    my_screen.screensize(width, height)
    my_pen = turtle.Turtle()
    my_screen.tracer(0)
    turtle.speed(10)

    # Printing Loop

    for i in range(int(height / 2), int(height / -2), -1):
        my_pen.penup()
        my_pen.goto(-(width / 2), i)

        for l in range(-int(width / 2), int(width / 2), 1):
            pix_width = int(l + (width / 2))
            pix_height = int(height / 2 - i)
            if img[pix_height, pix_width] == 0:
                my_pen.pendown()
                my_pen.forward(1)
            else:
                my_pen.penup()
                my_pen.forward(1)
        my_screen.update()

    my_pen.hideturtle()

    turtle.done()


def pixelizer(img: str, k_size):
    img = cv2.imread(img)
    grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    inverted_img = cv2.bitwise_not(grey_img)
    blurred_img = cv2.GaussianBlur(inverted_img, (k_size, k_size), 0)
    inverted_blurred_img = cv2.bitwise_not(blurred_img)
    img = cv2.divide(grey_img, inverted_blurred_img, scale=256.0)
    cv2.imwrite("sketch.png", img)


def draw_image_with_turtle(pixels):
    screen = turtle.Screen()
    screen.setup(width=len(pixels[0]), height=len(pixels))
    screen.setworldcoordinates(0, len(pixels), len(pixels[0]), 0)

    pen = turtle.Turtle()
    pen.speed(1)
    pen.penup()

    for y in range(len(pixels)):
        for x in range(len(pixels[0])):
            if pixels[y][x] == 1:  # Assuming 1 represents black and 0 represents white
                pen.goto(x, len(pixels) - y - 1)
                pen.dot()

    screen.exitonclick()


pixelizer("assets/licorne.png", 9)

draw_image_with_turtle(cv2.imread("sketch.png", 2))
