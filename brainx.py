import argparse
import sys

from brainx import brainfuck


__author__ = 'ivo'


def read_program():
    ret = str()
    for line in sys.stdin:
        ret = ret + line

    return ret


def is_code(program):
    program = str(program)
    return program.startswith("\"") and program.endswith("\"")


def is_file(program):
    program = str(program)
    return not (program.startswith("\"") and program.endswith("\""))


def read_program_from_file(filename):
    with open(filename) as f:
        return f.readlines()[0]  # jedna se o list, prvni polozka je string s programem


def create_log(program, memory, pointer, output, param):
    with open("debug\\debug_" + param + ".log", "w+") as f:
        f.write("# program data\n")
        f.write(program)
        f.write("\n\n# memory\n")
        f.write(str(memory))
        f.write("\n\n# memory pointer\n")
        f.write(str(pointer))
        f.write("\n\n# output\n")
        f.write(output)
        f.write("\n")


def next_log(num):
    if num[1] == "9":
        return chr(ord(num[0]) + 1) + "0"  # inkrementuje se desitkove cislo
    else:
        return num[0] + chr(ord(num[1]) + 1)  # desitkove se necha, jednotkove se inkrementuje


def log(program, memory, pointer, output):
    from os import listdir
    from os.path import isfile, join

    files = [f for f in listdir("debug\\") if isfile(join("debug\\", f))]
    if len(files) == 0:
        create_log(program, memory, pointer, output, "00")
    else:
        import re
        last = re.search("\d+", files[len(files) - 1]).group(0)
        create_log(program, memory, pointer, output, next_log(last))


def dispatch(program, memory=None, pointer=0, operation=None, debug=False):
    if not memory:
        memory = [0]

    if operation is None:
        output = brainfuck.interpret(program, memory, pointer)

    if debug:
        log(program, memory, pointer, output)


def load_program(data):
    program = str()
    if data is None:
        program = read_program()

    elif is_file(data):
        program = read_program_from_file(data)

    elif is_code(data):
        program = data

    return program


def parse_memory(memory):
    if (memory is None):
        return [0]
    return list(memory)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program", nargs="?", default=None)
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-m", "--memory", nargs="?", default=None)
    parser.add_argument("-p", "--pointer", nargs="+", default=0)
    args = parser.parse_args()

    program = load_program(args.program)
    memory = parse_memory(args.memory)
    pointer = int(args.pointer[0])

    dispatch(program, memory=memory, pointer=pointer, debug=args.test)


if __name__ == '__main__':
    main()