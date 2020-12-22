"""
File: my_drawing.py
Name: Danny Tsai
----------------------
This program can show a picture I draw, after few second,
it will show the origin version of this picture
"""
from campy.graphics.gobjects import GOval, GRect, GPolygon, GLabel
from campy.graphics.gwindow import GWindow
from simpleimage import SimpleImage
from campy.gui.events.timer import pause
import random
# Constant
SIZE = 6  # int, enlarge size of picture
PICTURE = 'images/all.png'  # Direction of origin picture
# Global variables
window = GWindow(width=100*SIZE, height=80*SIZE)


def main():
    """
    This program can show a picture I draw, after few second,
    it will show the origin version of this picture
    """
    make_rect(49, 40, 1, 39, 'navy')  # l_body
    make_rect(22, 28, 16, 16, 'white')  # l_beard
    make_rect(16, 20, 20, 20, 'peachpuff')  # l_head
    make_polygon(3, [(25, 1), (3, 17), (46, 17)], 'red')  # l_hat
    make_rect(40, 25, 53, 52, 'grey')  # r_body
    make_polygon(3, [(72, 28), (82, 28), (96, 57)], 'black')  # l_hair
    make_rect(20, 27, 52, 28, 'peachpuff')  # r_head
    make_rect(32, 15, 52, 13, 'darkgrey')  # r_hat
    label = GLabel('我全都要', x=window.width*0.25, y=window.height*0.9)
    label.color = 'magenta'
    label.font = '-{}'.format(10*SIZE)
    window.add(label)

    pause(3000)
    show_origin_picture()


def make_rect(width, height, x, y, color):
    """
    Draw a rect
    :param width: int, size of rect
    :param height: int, size of rect
    :param x: int, x coordinate
    :param y: int, y coordinate
    :param color: str, the color want to fill inside
    """
    global window
    rect = GRect(width*SIZE, height*SIZE, x=x*SIZE, y=y*SIZE)
    rect.filled = True
    rect.fill_color = color
    window.add(rect)


def make_polygon(num, coordinate, color):
    """
    Draw a polygon
    :param num: int, number of vertex
    :param coordinate: list, coordinate of every vertex :[(x1, y1), (x2, y2)...]
    :param color: str, the color want to fill inside
    """
    polygon = GPolygon()
    for i in range(num):
        x = coordinate[i][0] * SIZE
        y = coordinate[i][1] * SIZE
        polygon.add_vertex((x, y))
    window.add(polygon)
    polygon.filled = True
    polygon.fill_color = color


def show_origin_picture():
    """
    Draw the origin picture by following step:
    1.Get the info of origin picture.
    2.Draw it.
    """
    pixel_info = get_pixel_info()
    random.shuffle(pixel_info)
    for i in range(len(pixel_info)):
        make_rect_from_info(pixel_info[i])


def get_pixel_info():
    """
    Get information of every pixel in origin picture, and transform to drawable list.
    :return: list, [width, height, x, y, hex color code]
    """
    pixel_info = []
    img = SimpleImage(PICTURE)
    for x in range(img.width):
        for y in range(img.height):
            pixel = img.get_pixel(x, y)
            red = pixel.red
            green = pixel.green
            blue = pixel.blue
            color_hex = '0x{:02x}{:02x}{:02x}'.format(red, green, blue)
            pixel_info.append([SIZE, SIZE, x*SIZE, y*SIZE, color_hex])
    return pixel_info


def make_rect_from_info(information):
    """
    Draw a picture by using the information input.
    :param information: list, [width, height, x, y, color]
    """
    global window
    rect = GRect(information[0], information[1], x=information[2], y=information[3])
    rect.filled = True
    rect.fill_color = information[4]
    rect.color = information[4]
    window.add(rect)


if __name__ == '__main__':
    main()
