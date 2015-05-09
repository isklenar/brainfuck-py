import sys

import brainxlogger


__name__ = 'brainfuck'


def __parse_loops(program):
    """
    Zparsuje a namapuje smycky v bfuckovskem programu.
    :param program: zdrojovy kod v brainfucktu
    :return: dictiory, klicem je int, hodnotou je int. Hodnota je index odpovidajici smycky z indexu klice
    """
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


def get_input(program):
    """
    Pokud program obsahuje ! pro input, pripravy ho.
    :param program: bfuck program
    :return: input ze zdrojaku, None pokud neni.
    """
    data = program.split("!")
    if len(data) > 1:
        return data[1]

    return None


def interpret(program, memory=None, pointer=0, debug=False, width=0, rgb=None):  # width a rgb pro logovani
    """
    Intepretuje program v brainfucku.
    :param program: program k interpretace
    :param memory: pocatecni stav pameti
    :param pointer: pocatecni ukazatel do pameti
    :param debug: jestli se ma na konci vytvorit log
    :param width: sirka obrazku (pro logovani)
    :param rgb: rgb hodnoty obrazku (pro logovani)
    :return: vystup programu
    """
    if not memory:
        memory = [0]
    i = 0
    input = get_input(program)
    input_pointer = 0
    loops = __parse_loops(program)
    output = str()
    while i < len(program):
        if program[i] == ">":
            pointer += 1
            if pointer == len(memory):
                memory.append(0)

        elif program[i] == "<":
            if pointer > 0:
                pointer -= 1

        elif program[i] == "+":
            memory[pointer] = (memory[pointer] + 1) % 256  # overflow

        elif program[i] == "-":
            memory[pointer] = memory[pointer] - 1 if memory[pointer] - 1 >= 0 else 0  # underflow

        elif program[i] == ".":
            output += chr(memory[pointer])
            print(chr(memory[pointer]), end="")

        elif program[i] == ",":
            if input is None:
                character = sys.stdin.read(1)
                memory[pointer] = ord(character)
            else:
                memory[pointer] = ord(input[input_pointer])
                input_pointer += 1

        elif program[i] == "[":
            if memory[pointer] == 0:
                i = loops[i]

        elif program[i] == "]":
            if memory[pointer] != 0:
                i = loops[i]

        elif program[i] == "#":
            brainxlogger.log(program, memory, pointer, output, width, rgb)

        i += 1

    if debug:
        brainxlogger.log(program, memory, pointer, output, width, rgb)

    return output