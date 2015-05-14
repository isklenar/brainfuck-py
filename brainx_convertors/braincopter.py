from brainx_convertors.brainloller import __change_direction
from utils import png_reader

__author__ = 'ivo'
__name__ = "braincopter"


def __get_closest_colour(rgb, value):
    """
    Najde nejblizsi RGB hodnotu vstupnimu parametru.
    :param rgb:
    :param value:
    :return:
    """
    orig_value = (65536 * rgb[0] + 256 * rgb[1] + rgb[2]) % 11
    diff = abs(value - orig_value)

    if diff == 0:
        return rgb

    if 255 >= rgb[2] + 10 >= 0:  # padne do intervalu
        for x in range(11):
            new_val = (65536 * rgb[0] + 256 * rgb[1] + (rgb[2] + x)) % 11
            if new_val == value:
                return rgb[0], rgb[1], rgb[2] + x

    elif rgb[2] + 10 > 255:  # misto preteceni odecist
        for x in range(11):
            new_val = (65536 * rgb[0] + 256 * rgb[1] + (rgb[2] - x)) % 11
            if new_val == value:
                return rgb[0], rgb[1], rgb[2] - x


def __encode_command(rgb, command):
    """
    Zakoduje do pixelu prikaz brainfucku.
    :param rgb: RGB pixel
    :param command: brainfuck prikaz
    :return: zakodovane RGB prikazem
    """
    if command == ">": return __get_closest_colour(rgb, 0)
    if command == "<": return __get_closest_colour(rgb, 1)
    if command == "+": return __get_closest_colour(rgb, 2)
    if command == "-": return __get_closest_colour(rgb, 3)
    if command == ".": return __get_closest_colour(rgb, 4)
    if command == ",": return __get_closest_colour(rgb, 5)
    if command == "[": return __get_closest_colour(rgb, 6)
    if command == "]": return __get_closest_colour(rgb, 7)
    if command == "R_R": return __get_closest_colour(rgb, 8)
    if command == "R_L": return __get_closest_colour(rgb, 9)

    return __get_closest_colour(rgb, 10)


def __translate_pixel(rgb):
    """
    Prelozi RGB pixel braincopteru na prikaz brainfucku
    :param rgb: pixel
    :return: prikaz
    """

    value = (65536 * rgb[0] + 256 * rgb[1] + rgb[2]) % 11
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


def __create_row(rgb, program, program_pointer, pixel_pointer, width, x):
    ret = [(0, 0, 0) for x in range(width)]
    if x == 0:
        ret[0] = __encode_command(rgb[x * width], "NOP")
    else:
        ret[0] = __encode_command(rgb[x * width], "R_L")

    ret[width - 1] = __encode_command(rgb[x * width + width - 1], "R_R")

    for y in range(1, width - 1):
        if program_pointer >= len(program):
            command = "NOP"
        else:
            command = program[program_pointer]
            program_pointer += 1

        if x % 2 == 0:
            coords = y
        else:
            coords = width - 1 - y

        ret[coords] = __encode_command(rgb[x * width + coords], command)
        pixel_pointer += 1

    return ret, pixel_pointer, program_pointer


def __create_rgb_matrix(rgb, program, width, height):
    ret = [[] for x in range(height)]
    program_pointer = 0
    pixel_pointer = 0
    for x in range(0, height):
        ret[x], pixel_pointer, program_pointer = __create_row(rgb, program, program_pointer, pixel_pointer, width, x)

    return ret


def convert_program_to_image(program, filename, out):
    """
    Prelozi program do obrazku.
    :param program: program v brainfucku
    :param filename: cilovy obrazek
    :param out: jmeno ciloveho souboru
    """
    rgb, colours, width, height = png_reader.get_image(filename)
    if len(program) > len(rgb):
        return

    out_rgb = __create_rgb_matrix(rgb, program, width, height)

    return out_rgb, width, height


def convert_image_to_program(rgb, width, height):
    """
    Prelozi obrazek do programu.
    :param rgb: rgb hodnoty pixelu
    :param width: sirka obrazku
    :param height: vyska obrazku
    :return: program v brainfucku.
    """
    output = str()
    x_dir, y_dir = 1, 0  # jdeme na zacatku doprava

    x, y, i = 0, 0, 0
    while i < width * height:
        pixel = rgb[y * width + x]
        command = __translate_pixel(pixel)

        if command == "R_L" or command == "R_R":
            x_dir, y_dir = __change_direction(x_dir, y_dir, command)
        else:
            output += command

        x += x_dir
        y += y_dir

        i += 1

    return output