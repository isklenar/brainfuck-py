import zlib

from pngutils import PNGWrongHeaderError


__author__ = 'ivo'
__name__ = "png_reader"


def __read_png(filename):
    with open(filename, "rb") as f:
        while True:
            byte = f.read(1)
            if byte:
                yield byte
            else:
                break


def __check_header(data):
    if not (data[0] == b'\x89' and data[1] == b'P' and data[2] == b'N' and data[3] == b'G' and data[4] == b'\r' and
                    data[5] == b'\n'
            and data[6] == b'\x1a' and data[7] == b'\n'):
        raise PNGWrongHeaderError


def __read_chunks(data):
    p = 8  # prvnich 8B je hlavicka
    chunks = list()
    while p < len(data):
        length = int.from_bytes(data[p] + data[p + 1] + data[p + 2] + data[p + 3], byteorder='big')
        p += 4
        type = int.from_bytes(data[p] + data[p + 1] + data[p + 2] + data[p + 3], byteorder='big')

        p += 4

        chunkdata = b''
        for i in range(p, p + length):
            chunkdata += data[i]
            p += 1

        crc = int.from_bytes(data[p] + data[p + 1] + data[p + 2] + data[p + 3], byteorder='big')
        p += 4
        chunks.append((length, type, chunkdata, crc))

    return chunks


def __check_and_parse_first_chuck(chunk):
    data = chunk[2]

    width = int.from_bytes(data[0:4], byteorder="big")
    height = int.from_bytes(data[4:8], byteorder="big")

    return width, height


def __decompress(chunks):
    data = b''
    for i in range(1, len(chunks) - 1):
        data += chunks[i][2]

    return zlib.decompress(data)


def get_image(filename):
    data = list(__read_png(filename))

    __check_header(data)
    chunks = __read_chunks(data)
    width, height = __check_and_parse_first_chuck(chunks[0])
    image_data = __decompress(chunks)
    print()