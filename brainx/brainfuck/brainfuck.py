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


def interpret(program):
    memory = [0]
    pointer, i = 0, 0
    loops = __parse_loops(program)

    while pointer < len(program):
        if program[pointer] == ">":
            pointer += 1
            if pointer == len(memory):
                memory.append(0)

        if program[i] == "<":
            if pointer > 0:
                pointer -= 1

        if program[i] == "+":
            memory[pointer] = (memory[pointer] + 1) % 255  # overflow

        if program[i] == "-":
            memory[pointer] = memory[pointer] - 1 if memory[pointer] - 1 > 0 else 255  # underflow

        if program[i] == ".":
            print(memory[pointer])

        if program[i] == ",":
            character = sys.stdin.read(1)
            memory[pointer] = character

        if program[i] == "[":
            if memory[pointer] == 0:
                i = loops[i] + 1

        if program[i] == "]":
            if memory[pointer] != 0:
                i = loops[i] - 1 if loops[i] - 1 > 0 else 0

        i += 1


def interpret(program, mem=None):
    if not mem:
        mem = [0]
    memory = mem
    pointer, i = 0, 0
    loops = __parse_loops(program)

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