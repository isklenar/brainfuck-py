from brainx_convertors import braincopter, brainloller
import utils.png_reader


__author__ = 'ivo'
__name__ = "brain_image"


def translate(filename):
    """
    Prelozi obrazek v brainloller/copter variante do brainfucku.
    Vyhodi exception pokud PNG neni vporadku.

    :param filename: jmeno souboru
    :return: zdrojak v brainfucku, sirku obrazku a rgb hodnoty
    """
    rgb, colours, width, height = utils.png_reader.get_image(filename)

    if colours < 12:
        return brainloller.convert_image_to_program(rgb, width, height), width, rgb
    else:
        return braincopter.convert_image_to_program(rgb, width, height), width, rgb

