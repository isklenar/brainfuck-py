import argparse
import ast
import os
import sys

from brainx import brainfuck
from brainx import brain_image
from brainx_convertors import brainloller
from brainx_convertors import braincopter
from utils import png_writer


__author__ = 'ivo'


def read_program():
    ret = str()
    for line in sys.stdin:
        ret = ret + line

    return ret


def is_code(program):
    program = str(program)
    return program.startswith("\"") and program.endswith("\"")


def is_file(filename):
    return os.path.isfile(filename)


def read_program_from_file(filename):
    extension = filename.split(".")
    extension = extension[len(extension) - 1]
    if extension == "b":
        with open(filename) as f:
            return "".join(f.readlines()), 0, None, False
    else:
        program, width, rgb = brain_image.translate(filename)
        return program, width, rgb, True


def execute(program, memory=None, pointer=0, debug=False, width=0, rgb=None):
    if not memory:
        memory = [0]

    output = brainfuck.interpret(program, memory, pointer, debug=debug, width=width, rgb=rgb)

    return output


def load_program(data):
    if isinstance(data, list): # z argparse prijde list
        data = data[0]

    program = str(data)
    is_image = False
    rgb = None
    width = 0
    if data is None:
        program = read_program()

    if is_file(data):
        program, width, rgb, is_image = read_program_from_file(data)

    return strip_program(program), width, rgb, is_image


def parse_memory(memory):
    memory = ast.literal_eval(memory)
    return [int(x) for x in memory]


def determine_operation(args):
    if args.lc2f is not None:
        return "ItF"

    if args.f2lc and len(args.i) == 1:
        return "FtIBL"

    if args.f2lc and len(args.i) == 2:
        return "FtIBC"

    return "ex"


def strip_program(program):
    allowed_commands = [">", "<", "+", "-", "[", "]", ",", ".", "!", "#"]
    ret = ""
    input = False
    for x in program:  # arg je tuple s programem a barvou
        if x == "!":
            input = True
            ret += x
        elif input:
            ret += x
        elif x in allowed_commands:
            ret += x

    return ret


def dispatch(operation, args):
    if operation == "ItF":
        program = brain_image.translate(args.lc2f[0])
        if args.lc2f[1].startswith(">"):
            print(program)
        else:
            with open(args.lc2f[1], "w") as f:
                f.write(program)

    elif operation == "ex":
        program, width, rgb, image = load_program(args.program)
        memory = parse_memory(args.memory)
        pointer = int(args.memory_pointer[0])

        execute(program, memory=memory, pointer=pointer, debug=args.test, width=width, rgb=rgb)

    elif operation == "FtIBL":
        program = load_program(args.i[0])
        rgb, width, height = brainloller.convert_program_to_image(program)
        png_writer.write_png(args.o, rgb, width, height)

    elif operation == "FtIBC":
        program = load_program(args.i[0])
        rgb, width, height = braincopter.convert_program_to_image(program, args.i[1])
        png_writer.write_png(args.o, rgb, width, height)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program", nargs="?", default=None)
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-m", "--memory", default="b'\\0'")
    parser.add_argument("-p", "--memory-pointer", nargs=1, default=[0])
    parser.add_argument("--lc2f", nargs=2)
    parser.add_argument("--f2lc", action="store_true")
    parser.add_argument("-i", nargs="+")
    parser.add_argument("-o", nargs=1)
    parser.add_argument("---pnm", "--pbm", action="store_true")

    args = parser.parse_args()
    operation = determine_operation(args)
    dispatch(operation, args)
    sys.exit(0)


if __name__ == '__main__':
    main()