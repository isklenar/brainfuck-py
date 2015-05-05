import argparse
import ast
import sys

from brainx import brainfuck
from brainx import brain_image
from brainx import brainxlogger
from brainx_convertors import brainloller
from brainx_convertors import braincopter
from pngutils import png_writer


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
    extension = filename.split(".")
    extension = extension[len(extension) - 1]
    if extension == "b":
        with open(filename) as f:
            return "".join(f.readlines())  # jedna se o list, prvni polozka je string s programem
    else:
        return brain_image.translate(filename)


def execute(program, memory=None, pointer=0, operation=None, debug=False):
    if not memory:
        memory = [0]

    output = ""

    if operation is None:
        output = brainfuck.interpret(program, memory, pointer)

    if debug:
        brainxlogger.log(program, memory, pointer, output)


def load_program(data):
    program = str()
    if data is None:
        return read_program()

    if is_file(data):
        return read_program_from_file(data)

    if is_code(data):
        return data

    return program


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


def dispatch(operation, args):
    if operation == "ItF":
        program = brain_image.translate(args.lc2f[0])
        if args.lc2f[1].startswith(">"):
            print(program)
        else:
            with open(args.lc2f[1], "w") as f:
                f.write(program)

    elif operation == "ex":
        program = load_program(args.program)
        memory = parse_memory(args.memory)
        pointer = args.memory_pointer

        execute(program, memory=memory, pointer=pointer, debug=args.test)

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
    parser.add_argument("-p", "--memory-pointer", nargs=1, default=0)
    parser.add_argument("--lc2f", nargs=2)
    parser.add_argument("--f2lc", action="store_true")
    parser.add_argument("-i", nargs="+")
    parser.add_argument("-o", nargs=1)

    args = parser.parse_args()
    operation = determine_operation(args)
    dispatch(operation, args)
    sys.exit(0)


if __name__ == '__main__':
    main()