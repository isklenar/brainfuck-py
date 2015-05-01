import sys

__name__ = 'brainfuck'


def __parse_loops(program):
    ret = {}
    stack = []

    i = 0
    while i < len(program):
        if program[i] == "[":
            stack.append(i)

        if program[i] == "]":
            start = stack.pop()
            ret[i] = start
            ret[start] = i

        i += 1

    return ret


def interpret(program, memory=[0], pointer=0):
    i = 0
    loops = __parse_loops(program)
    output = str()
    while i < len(program):
        if program[i] == ">":
            pointer += 1
            if pointer == len(memory):
                memory.append(0)

        if program[i] == "<":
            if pointer > 0:
                pointer -= 1

        if program[i] == "+":
            memory[pointer] = (memory[pointer] + 1) % 255  # overflow

        if program[i] == "-":
            memory[pointer] = memory[pointer] - 1 if memory[pointer] - 1 > 0 else 0  # underflow

        if program[i] == ".":
            output += chr(memory[pointer])
            print(chr(memory[pointer]))

        if program[i] == ",":
            character = sys.stdin.read(1)
            memory[pointer] = int(character)

        if program[i] == "[":
            if memory[pointer] == 0:
                i = loops[i] + 1

        if program[i] == "]":
            if memory[pointer] != 0:
                i = loops[i] - 1 if loops[i] - 1 > 0 else 0

        i += 1

    return output