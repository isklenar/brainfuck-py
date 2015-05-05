import argparse
import ast
import sys

from brainx import brainfuck
from brainx import brain_image
from brainx import brainxlogger
from brainx_convertors import brainloller
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program", nargs="?", default=None)
    parser.add_argument("-t", "--test", action="store_true")
    parser.add_argument("-m", "--memory", default="b'\\0'")
    parser.add_argument("-p", "--memory-pointer", nargs=1, default=0)
    parser.add_argument("--lc2f")
    args = parser.parse_args()

    program = load_program(args.program)
    memory = parse_memory(args.memory)
    pointer = args.memory_pointer
    rgb, width, height = brainloller.convert_program_to_image(program)
    png_writer.write_png("test.png", rgb, width, height)
    execute(program, memory=memory, pointer=pointer, debug=args.test)


if __name__ == '__main__':
    main()