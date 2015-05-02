import braincopter
import pngutils.png_reader
import brainloller

__author__ = 'ivo'
__name__ = "brain_image"


def translate(filename):
    rgb, colours, width, height = pngutils.png_reader.get_image(filename)

    if colours < 12:
        return brainloller.translate(rgb, width, height)
    else:
        return braincopter.translate(rgb, width, height)