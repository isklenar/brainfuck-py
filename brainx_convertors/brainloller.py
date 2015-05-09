import math

__author__ = 'ivo'
__name__ = "brainloller"


def __translate_pixel(r, g, b):
    """
    Prelozi pixel na prikaz.
    :param r: hodnota cervene
    :param g: hodnota zelene
    :param b: hodnota modre
    :return: prikaz
    """
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
    """
    Prelozi prikaz na RGB tuple.
    :param command: prikaz
    :return: RGB tuple
    """
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
    """
    Zmeni smer cteni podle aktuaniho smeru a pozadavku
    :param x_dir: aktualni smer x
    :param y_dir:  aktualni smer y
    :param command: prikaz zmeny
    :return: novy smer x, novy smer y
    """

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
    """
    Prevede obrazek do programu
    :param rgb: rgb hodnoty obrazku
    :param width: sirka
    :param height: vyska
    :return: brainfuckovsky program
    """

    output = str()
    x_dir, y_dir = 1, 0  # jdeme na zacatku doprava

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


def __find_nearest_larger_square(number):
    """
    Najde neblizsi x takove, aby x**2 > arg.
    :param number: cislo
    :return: nejblizsi vetsi ctverec
    """
    return math.ceil(math.sqrt(number) + 1)


def convert_program_to_image(program):
    """
    Prevede program do obrazku ve variante brainloller.
    :param program: program v brainfucku
    :return: 2D list rgb hodnotu, sirku a vysku
    """

    n = __find_nearest_larger_square(len(program))
    ret = [[(0, 0, 0) for x in range(n + 2)] for x in range(n)]

    for i in range(0, n, 2):  # sude radky, cteme zleva doprava
        for j in range(n):
            if i * n + j >= len(program):
                ret[i][j + 1] = __translate_command("NOP")
            else:
                ret[i][j + 1] = __translate_command(program[i * n + j])

    for i in range(1, n, 2):  # liche radky, cteme zprava doleva
        for j in range(n):
            if i * n + j >= len(program):
                ret[i][n - 1 - j] = __translate_command("NOP")
            else:
                ret[i][n - j] = __translate_command(program[i * n + j])

    for i in range(n):  # okraje jsou rotace
        if i == 0:
            ret[i][0] = __translate_command("NOP")
        else:
            ret[i][0] = __translate_command("R_L")

        ret[i][n + 1] = __translate_command("R_R")

    return ret, n + 2, n
