import sys

from brainx_convertors import braincopter, brainloller
from utils import PNGWrongHeaderError
from utils.PNGNotImplementedError import PNGNotImplementedError
import utils.png_reader


__author__ = 'ivo'
__name__ = "brain_image"


def translate(filename):
    try:
        rgb, colours, width, height = utils.png_reader.get_image(filename)

        if colours < 12:
            return brainloller.convert_image_to_program(rgb, width, height)
        else:
            return braincopter.convert_image_to_program(rgb, width, height)
    except PNGWrongHeaderError:
        sys.exit(4)
    except PNGNotImplementedError:
        sys.exit(8)
