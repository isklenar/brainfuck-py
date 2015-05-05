import zlib
import struct

__author__ = 'ivo'
__name__ = "png_writer"


def __create_header():
    return b'\x89PNG\r\n\x1a\n'


def __create_head_chunk(width, height):
    length = b'\x00\x00\x00\r'  # 13
    chunk_name = b'IHDR'
    dim = struct.pack(">I", width) + struct.pack(">I", height)
    options = b'\x08\x02\x00\x00\x00'

    data = length + chunk_name + dim + options
    crc = zlib.crc32(dim + options)

    return data + struct.pack(">I", crc)


def __create_end_chunk():
    length = b'\x00\x00\x00\00'  # 0
    chunk_name = b'IEND'
    data = b''
    crc = b'\xaeB`\x82'

    return length + chunk_name + data + crc


def __create_data_chunk(rgb, width, height):
    chunk_name = b'IDAT'
    data = b''

    for i in range(height):
        data += b'\0'  # filt
        for j in range(width):
            data += struct.pack(">B", rgb[i][j][0]) + struct.pack(">B", rgb[i][j][1]) + struct.pack(">B", rgb[i][j][2])

    data = zlib.compress(data)

    length = len(data)

    out = struct.pack(">I", length) + chunk_name + data
    out += struct.pack(">I", zlib.crc32(out))

    return out


def write_png(filename, rgb, width, height):
    header = __create_header()
    head_chunk = __create_head_chunk(width, height)

    data_chunk = __create_data_chunk(rgb, width, height)

    end_chunk = __create_end_chunk()

    to_write = header + head_chunk + data_chunk + end_chunk

    with open(filename, "bw") as f:
        f.write(to_write)
