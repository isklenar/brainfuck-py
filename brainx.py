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
        return f.readlines()


def dispatch(program, memory=None, pointer=0, operation=None):
    if not memory:
        memory = [0]

    if operation is None:
        brainfuck.interpret(program, memory, pointer)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("program", nargs="?", default=None)

    args = parser.parse_args()
    program = str()

    if args.program is None:
        program = read_program()

    elif is_file(args.program):
        program = read_program_from_file(program)

    elif is_code(args.program):
        program = args.program

    dispatch(program)


if __name__ == '__main__':
    main()