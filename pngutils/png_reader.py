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


def __paeth(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)

    if pa <= pb and pa <= pc:
        pr = a
    elif pb <= pc:
        pr = b
    else:
        pr = c

    return pr


def rgb_data(tmp, f, pa=None, pb=None, pc=None):
    r = int.from_bytes(tmp[:1], byteorder="big")
    g = int.from_bytes(tmp[1:2], byteorder="big")
    b = int.from_bytes(tmp[2:3], byteorder="big")

    if f == 0:
        return r, g, b

    if f == 1:
        r += pa[0]
        g += pa[1]
        b += pa[2]

    if f == 2:
        r += pb[0]
        g += pb[1]
        b += pb[2]

    if f == 3:
        r += ((pa[0] + pb[0]) / 2)
        g += ((pa[1] + pb[1]) / 2)
        b += ((pa[2] + pb[2]) / 2)

    if f == 4:
        r += __paeth(pa[0], pb[0], pc[0])
        g += __paeth(pa[1], pb[1], pc[1])
        b += __paeth(pa[2], pb[2], pc[2])

    return r & 0xFF, g & 0xFF, b & 0xFF


def create_rgb_matrix(image_data, width, height):
    ret = [0 for x in range(0, height * width)]

    for x in range(height):
        f = int.from_bytes(image_data[:1], byteorder="big")
        image_data = image_data[1:]
        for y in range(width):
            tmp = image_data[:3]
            image_data = image_data[3:]

            a = ret[x * width + y - 1] if y > 0 else (0, 0, 0)
            b = ret[(x - 1) * width + y] if x > 0 else (0, 0, 0)
            c = ret[(x - 1) * width + y - 1] if x > 0 and y > 0 else (0, 0, 0)
            rgb = rgb_data(tmp, f, a, b, c)

            ret[x * width + y] = rgb

    return ret


def get_image(filename):
    data = list(__read_png(filename))

    __check_header(data)
    chunks = __read_chunks(data)
    width, height = __check_and_parse_first_chuck(chunks[0])
    image_data = __decompress(chunks)
    return create_rgb_matrix(image_data, width, height), width, height