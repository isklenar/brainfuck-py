import zlib

__author__ = 'ivo'
__name__ = "png_writer"


def __create_header():
    return b'\x89PNG\r\n\x1a\n'


def __create_head_chunk(n):
    length = b'\x00\x00\x00\r'  # 13
    chunk_name = b'IHDR'
    dim = str(n).encode()
    options = b'\x08\x02\x00\x00\x00'

    data = length + chunk_name + dim + options
    crc = zlib.crc32(data)

    return data + crc


def __create_end_chunk():
    length = b'\x00\x00\x00\00'  # 0
    chunk_name = b'IEND'
    data = b''
    crc = b'\xaeB`\x82'

    return length + chunk_name + data + crc


def __create_data_chunk(rgb):
    data = b''



def write_png(filename, rgb, n):
    header = __create_header()
    head_chunk = __create_head_chunk(n)

    data_chunk = __create_data_chunk(rgb)

    end_chunk = __create_end_chunk()
