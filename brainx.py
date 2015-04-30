import argparse

__author__ = 'ivo'


def read_program():
    return None


def execute(filename):
    pass


def main():
    print("hello")
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    if args.filename is None:
        program = read_program()
    else:
        execute(args.filename)


if __name__ == '__main__':
    main()