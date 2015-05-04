import math

__author__ = 'ivo'
__name__ = "brainloller"


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


def __translate_command(command):
    if command == ">":
        return 255, 0, 0
    elif command == "<":
        return 128, 0, 0
    elif command == "+":
        return 0, 255, 0
    elif command == "-":
        return 0, 128, 0
    elif command == ".":
        return 0, 0, 255
    elif command == ",":
        return 0, 0, 128
    elif command == "[":
        return 255, 255, 0
    elif command == "]":
        return 128, 128, 0
    elif command == "R_R":
        return 0, 255, 255
    elif command == "R_L":
        return 0, 128, 128

    return 0, 0, 0


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


def convert_image_to_program(rgb, width, height):
    output = str()
    x_dir, y_dir = 1, 0  # jdeme na zacatku doprava

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


def __find_nearest_larger_square(number):
    return math.ceil(math.sqrt(number) + 1)


def convert_program_to_image(program):
    ret = []

    n = len(program)
    for i in range(0, n):
        rgb = __translate_command(program[i])
        ret.append(rgb)

    return ret, n