__author__ = 'ivo'
__name__ = "brainloller"

import pngutils.png_reader


def __translate_pixel(r, g, b):
    if r == 255 and g == 0 and b == 0:   return ">"
    if r == 128 and g == 0 and b == 0:   return "<"
    if r == 0 and g == 255 and b == 0:   return "+"
    if r == 0 and g == 128 and b == 0:   return "-"
    if r == 0 and g == 0 and b == 255: return "."
    if r == 0 and g == 0 and b == 128: return ","
    if r == 255 and g == 255 and b == 0:   return "["
    if r == 128 and g == 128 and b == 0:   return "]"
    if r == 0 and g == 255 and b == 255: return "R_R"
    if r == 0 and g == 128 and b == 128: return "R_L"

    return ""


def __change_direction(x_dir, y_dir, command):
    if command == "R_L":
        if x_dir == 1 and y_dir == 0: return 0, -1  # jdeme doprava, novy smer dolu
        if x_dir == 0 and y_dir == 1: return 1, 0  # jdeme dolu, novy smer doprava
        if x_dir == -1 and y_dir == 0: return 0, 1  # jdeme doleva, novy smer nahoru
        if x_dir == 0 and y_dir == -1: return -1, 0  # jdeme nahoru, novy smer doleva

    if command == "R_R":
        if x_dir == 1 and y_dir == 0: return 0, 1  # jdeme doprava, novy smer nahoru
        if x_dir == 0 and y_dir == 1: return -1, 0  # jdeme dolu, novy smer doleva
        if x_dir == -1 and y_dir == 0: return 0, -1  # jdeme doleva, novy smer nahoru
        if x_dir == 0 and y_dir == -1: return 1, 0  # jdeme nahoru, novy smer doprava

    return x_dir, y_dir


def read_png_program(filename):
    output = str()
    x_dir, y_dir = 1, 0  # jdeme na zacatku doprava

    rgb, width, height = pngutils.png_reader.get_image(filename)

    x, y, i = 0, 0, 0

    while i < width * height:
        r, g, b = rgb[y*width + x]
        command = __translate_pixel(r, g, b)

        if command == "R_L" or command == "R_R":
            x_dir, y_dir = __change_direction(x_dir, y_dir, command)
        else:
            output += command

        x += x_dir
        y += y_dir

        i += 1

    return output