__author__ = 'ivo'
__name__ = "brainxlogger"


def __next_log(num):
    if num[1] == "9":
        return chr(ord(num[0]) + 1) + "0"  # inkrementuje se desitkove cislo
    else:
        return num[0] + chr(ord(num[1]) + 1)  # desitkove se necha, jednotkove se inkrementuje


def __rgb_to_str(rgb, width):
    out = "# RGB input\n[\n"
    if rgb is None:
        return ""

    height = int(len(rgb) / width)

    for x in range(height):
        out += "    ["
        separator = ""
        for y in range(width):
            out += separator + str(rgb[x * width + y])
            if y == 0:
                separator = ", "

        out += "],\n"
    out += "]\n"
    return out + "\n"


def __create_log(program, memory, pointer, output, num, width, rgb):
    import array

    mem_out = array.array("B", memory).tostring()

    with open("debug\\debug_" + num + ".log", "w+") as f:
        f.write("# program data\n")
        f.write(program)
        f.write("\n\n# memory\n")
        f.write(str(mem_out))
        f.write("\n\n# memory pointer\n")
        f.write(str(pointer))
        f.write("\n\n# output\n")
        f.write(str(str.encode(output)))
        f.write("\n\n")
        f.write(__rgb_to_str(rgb, width))


def log(program, memory, pointer, output, width, rgb):
    from os import listdir
    from os.path import isfile, join

    files = [f for f in listdir("debug\\") if isfile(join("debug\\", f))]
    if len(files) == 0:
        __create_log(program, memory, pointer, output, "01", width, rgb)
    else:
        import re

        last = re.search("\d+", files[len(files) - 1]).group(0)
        __create_log(program, memory, pointer, output, __next_log(last), width, rgb)