__author__ = 'ivo'
__name__ = "brainxlogger"


def __next_log(num):
    if num[1] == "9":
        return chr(ord(num[0]) + 1) + "0"  # inkrementuje se desitkove cislo
    else:
        return num[0] + chr(ord(num[1]) + 1)  # desitkove se necha, jednotkove se inkrementuje


def __create_log(program, memory, pointer, output, param):
    import array
    mem_out = array.array("B", memory).tostring()

    with open("debug\\debug_" + param + ".log", "w+") as f:
        f.write("# program data\n")
        f.write(program)
        f.write("\n\n# memory\n")
        f.write(str(mem_out))
        f.write("\n\n# memory pointer\n")
        f.write(str(pointer))
        f.write("\n\n# output\n")
        f.write(str(str.encode(output)))
        f.write("\n\n")


def log(program, memory, pointer, output):
    from os import listdir
    from os.path import isfile, join

    files = [f for f in listdir("debug\\") if isfile(join("debug\\", f))]
    if len(files) == 0:
        __create_log(program, memory, pointer, output, "01")
    else:
        import re

        last = re.search("\d+", files[len(files) - 1]).group(0)
        __create_log(program, memory, pointer, output, __next_log(last))