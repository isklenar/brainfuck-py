import sys

__name__ = 'brainfuck'


def interpret(program):
    memory = [0]
    pointer = 0
    i = 0

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


def interpret(program, memory):
    pass