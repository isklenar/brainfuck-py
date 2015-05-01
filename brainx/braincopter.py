from brainloller import __change_direction

__author__ = 'ivo'
__name__ = "braincopter"

import pngutils.png_reader


def __translate_pixel(r, g, b):
    value = (65536 * r + 256 * g + b) % 11
    if value == 0: return ">"
    if value == 1: return "<"
    if value == 2: return "+"
    if value == 3: return "-"
    if value == 4: return "."
    if value == 5: return ","
    if value == 6: return "["
    if value == 7: return "]"
    if value == 8: return "R_R"
    if value == 9: return "R_L"

    return ""


def read_png_program(filename):
    output = str()
    x_dir, y_dir = 1, 0  # jdeme na zacatku doprava

    rgb, width, height = pngutils.png_reader.get_image(filename)

    x, y, i = 0, 0, 0

    while i < width * height:
        r, g, b = rgb[y * width + x]
        command = __translate_pixel(r, g, b)

        if command == "R_L" or command == "R_R":
            x_dir, y_dir = __change_direction(x_dir, y_dir, command)
        else:
            output += command

        x += x_dir
        y += y_dir

        i += 1

    return output