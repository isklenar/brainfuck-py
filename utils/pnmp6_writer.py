import struct

__author__ = 'ivo'
__name____ = "pnmp6_writer"


def write_pnm(filename, rgb, width, height):
    header = b'P6 ' + struct.pack("I", width) + b' ' + struct.pack("I", height) + b' ' + struct.pack("I", 255) + b' '
    data = b''
    for x in range(len(rgb)):
        data += struct.pack("B", rgb[x][0]) + struct.pack("B", rgb[x][1]) + struct.pack("B", rgb[x][2])

    data = header + data

    with open(filename, "bw") as f:
        f.write(data)
