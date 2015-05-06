from brainx_convertors.brainloller import __change_direction
from utils import png_reader

__author__ = 'ivo'
__name__ = "braincopter"


def get_closest_colour(rgb, value):
    orig_value = __translate_pixel(rgb)
    diff = value - orig_value

    if diff == 0:
        return rgb

    diff = abs(diff)

    if rgb[2] + diff > 255:
        return rgb[0], rgb[1], rgb[2] - diff
    else:
        return rgb[0], rgb[1], rgb[2] + diff



def __encode_command(rgb, command):
    if command == ">": return get_closest_colour(rgb, 0)
    if command == "<": return get_closest_colour(rgb, 1)
    if command == "+": return get_closest_colour(rgb, 2)
    if command == "-": return get_closest_colour(rgb, 3)
    if command == ".": return get_closest_colour(rgb, 4)
    if command == ",": return get_closest_colour(rgb, 5)
    if command == "[": return get_closest_colour(rgb, 6)
    if command == "]": return get_closest_colour(rgb, 7)
    if command == "R_R": return get_closest_colour(rgb, 8)
    if command == "R_L": return get_closest_colour(rgb, 9)

    return get_closest_colour(rgb, 10)


def __translate_pixel(rgb):
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


def convert_program_to_image(program, filename):
    rgb = png_reader.get_image(filename)
    if len(program) > len(rgb):
        return  # @TODO dodelat

    for x in range(len(rgb)):
        if x >= len(program):
            break

        rgb[x] = __encode_command(rgb, program[x])

    return rgb


def convert_image_to_program(rgb, width, height):
    output = str()
    x_dir, y_dir = 1, 0  # jdeme na zacatku doprava

    x, y, i = 0, 0, 0
    while i < width * height:
        rgb = rgb[y * width + x]
        command = __translate_pixel(rgb)

        if command == "R_L" or command == "R_R":
            x_dir, y_dir = __change_direction(x_dir, y_dir, command)
        else:
            output += command

        x += x_dir
        y += y_dir

        i += 1

    return output