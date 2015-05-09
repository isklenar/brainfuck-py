from brainx_convertors import braincopter, brainloller
import utils.png_reader


__author__ = 'ivo'
__name__ = "brain_image"


def translate(filename):
    rgb, colours, width, height = utils.png_reader.get_image(filename)

    if colours < 12:
        return brainloller.convert_image_to_program(rgb, width, height), width, rgb
    else:
        return braincopter.convert_image_to_program(rgb, width, height), width, rgb

