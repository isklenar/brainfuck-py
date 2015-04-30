import argparse

from brainx.brainfuck import brainfuck


__author__ = 'ivo'


def read_program():
    return None


def execute(filename):
    pass


def main():
    brainfuck.interpret(",++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.")
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?")
    args = parser.parse_args()

    if args.filename is None:
        program = read_program()
    else:
        execute(args.filename)


if __name__ == '__main__':
    main()