import zlib

from utils import PNGWrongHeaderError
from utils import PNGNotImplementedError


__author__ = 'ivo'
__name__ = "png_reader"


def __read_png(filename):
    """
    Precte vsechny byty souboru
    :param filename: jmeno souboru
    :return: byty souboru
    """
    with open(filename, "rb") as f:
        while True:
            byte = f.read(1)
            if byte:
                yield byte
            else:
                break


def __check_header(data):
    """
    Zkontroluje PNG header.
    Vyhodi PNGWrongHeaderError pokud je header spatny.
    :param data: hlavicka
    """
    if not (data[0] == b'\x89' and data[1] == b'P' and data[2] == b'N' and data[3] == b'G' and data[4] == b'\r' and
                    data[5] == b'\n' and data[6] == b'\x1a' and data[7] == b'\n'):
        raise PNGWrongHeaderError


def __read_chunks(data):
    """
    Precte vsechny chunky PNG
    :param data: bytove data
    :return: list chunku (chunk = tuple(delka, typ, data, crc))
    """
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


def __check_settings(data):
    """
    Zkontroluje ze PNG je ve formatau specifikace.
    Vyhodi PNGNotImplementedError pokud neni.
    :param data: data
    """
    if not (data[0:1] == b'\x08' and data[1:2] == b'\x02' and data[2:3] == b'\x00'and data[3:4] == b'\x00' and data[4:5] == b'\x00'):
        raise PNGNotImplementedError


def __check_and_parse_first_chunk(chunk):
    """
    Zkottroluje hlavickovy chunk.
    :param chunk: hlavickovy chunk
    :return: sirku, vysku
    """
    data = chunk[2]  # hlavickovy chunk je tuple, 3 polozka jsou data

    width = int.from_bytes(data[0:4], byteorder="big")
    height = int.from_bytes(data[4:8], byteorder="big")

    data = data[8:13]

    __check_settings(data)

    return width, height


def __decompress(chunks):
    """
    Pomoci zlib decompresne data chunku a spoji do jednoho
    :param chunks: list chunku
    :return: RGB dekompresovane hodnoty
    """
    data = b''
    for i in range(1, len(chunks) - 1):
        data += chunks[i][2]  # treti polozka jsou data

    return zlib.decompress(data)


def __paeth(a, b, c):
    """
    Provede paeth filtraci nad 3 hodnotami
    """
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


def __rgb_data(tmp, f, pa=None, pb=None, pc=None):
    """
    Prevede 3 byty na rgb hodnotu podle filtrace
    :param tmp: data rgb
    :param f: png filtr
    :param pa: a ve filtru
    :param pb: b ve filtru
    :param pc: c ve filtru
    :return: cervena, zelena, modra jako int tuple
    """
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

    return r % 256, g % 256, b % 256


def create_rgb_matrix(image_data, width, height):
    """
    Vytvori RGB matici z raw bytu.
    :param image_data: rgb data obrazku
    :param width: sirka
    :param height: vyska
    :return: RGB matice, pocet barev
    """
    ret = [(0, 0, 0) for x in range(0, height * width)]
    colours = {}
    p = 0
    for x in range(height):
        f = int.from_bytes(image_data[p: p + 1], byteorder="big")
        p += 1

        for y in range(width):
            tmp = image_data[p:p + 3]

            p += 3
            a = ret[x * width + y - 1] if y > 0 else (0, 0, 0)
            b = ret[(x - 1) * width + y] if x > 0 else (0, 0, 0)
            c = ret[(x - 1) * width + y - 1] if x > 0 and y > 0 else (0, 0, 0)
            rgb = __rgb_data(tmp, f, a, b, c)

            if colours.get(rgb) is None:
                colours[rgb] = 1
            else:
                colours[rgb] += 1

            ret[x * width + y] = rgb

    return ret, len(colours.keys())


def get_image(filename):
    """
    Precte obrazek a vraci ho jako RGB matici.
    :param filename: jmeno souboru
    :return: rgb, pocet barev, sirka, vyska
    """
    data = list(__read_png(filename))

    __check_header(data)

    chunks = __read_chunks(data)
    width, height = __check_and_parse_first_chunk(chunks[0])
    image_data = __decompress(chunks)

    rgb, colours = create_rgb_matrix(image_data, width, height)

    return rgb, colours, width, height