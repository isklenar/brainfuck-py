﻿#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tento testovací skript předpokládá, že výkonná část interpretru je uložena v adresáři „brainx“ (a tudíž volána pomocí „__main__.py“). Souhrnně je adresářová struktura semestrálky následující:

semestrálka.kostra/
    brainx/
        __main__.py
        ...
    tests/
        ...
    README.txt
    tests.py

Postupně se volají následující testy:

# memory tests
brainx "[-]" -m b'\x03\x02' -p 1 -t
brainx "[[-]<]" -m b'\x03\x03\x00\x02\x02' -p 4 -t
brainx "[<]" -m b'\x03\x03\x00\x02\x02' -p 4 -t
brainx "[>]" -m b'\x03\x03\x00\x02\x02' -t
brainx "[>+<-]" -m b'\x03\x03' -t
brainx "[>+>+<<-]>>[<<+>>-]" -m b'\x03\x03' -t
brainx "[>-<-]" -m b'\x03\x05' -t

# basic brainfuck tests
brainx tests/hello1.b
brainx tests/hello2.b
brainx -t tests/hello2.b
brainx tests/hello2t.b

# brainfuck with input
brainx tests/numwarp_input.b

# basic PNG
brainx tests/sachovnice.jpg
brainx tests/sachovnice_paleta.png

# brainloller
brainx tests/HelloWorld.png
brainx -t tests/HelloWorld.png

"""


import subprocess
from time import sleep


def clean():
    import shutil
    import os
    sleep(0.2)
    if os.path.exists("debug"):
        shutil.rmtree("debug/")

    sleep(0.2)
    if not os.path.exists("debug"):
        os.makedirs("debug")

#
# memory tests
#
#
clean()
# test 0a
print('\n\nTest 0a: brainx "[-]" -m b\'\\x03\\x02\' -p 1 -t')
print('\tvynulování aktuální, ale pouze aktuální, buňky')
args = 'python brainx.py [-] -m b\'\\x03\\x02\' -p 1 -t'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode)
assert p.returncode == 0
print( "error:", error )
assert error == b''
with open('tests/memory01_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out


clean()
# test 0b
print('\n\nTest 0b: brainx "[[-]<]" -m b\'\\x03\\x03\\x00\\x02\\x02\' -p 4 -t')
print('\tvynulování všech nenulových buněk doleva')
args = 'python brainx.py [[-]<] -m b\'\\x03\\x03\\x00\\x02\\x02\' -p 4 -t'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory02_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
clean()
# #
# # test 0c
print('\n\nTest 0c: brainx "[<]" -m b\'\\x03\\x03\\x00\\x02\\x02\' -p 4 -t')
print('\tpřesun na první nenulovou buňku doleva')
args = 'python brainx.py [<] -m b\'\\x03\\x03\\x00\\x02\\x02\' -p 4 -t'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory03_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
clean()
# #
# # # test 0d
print('\n\nTest 0d: brainx "[>]" -m b\'\\x03\\x03\\x00\\x02\\x02\' -t')
print('\tpřesun na první nenulovou buňku doprava')
args = 'python brainx.py [>] -m b\'\\x03\\x03\\x00\\x02\\x02\' -t'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory04_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
clean()
# test 0e
print('\n\nTest 0e: brainx "[>+<-]" -m b\'\\x03\\x03\' -t')
print('\tdestruktivní přičtení aktuální buňky k buňce následující')
args = 'python brainx.py [>+<-] -m b\'\\x03\\x03\' -t'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory05_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
clean()
# test 0f
print('\n\nTest 0f: brainx "[>+>+<<-]>>[<<+>>-]" -m b\'\\x03\\x03\' -t')
print('\tnedestruktivní přičtení aktuální buňky k buňce následující')
args = 'python brainx.py [>+>+<<-]>>[<<+>>-] -m b\'\\x03\\x03\' -t'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory06_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
clean()
# test 0g
print('\n\nTest 0g: brainx "[>-<-]" -m b\'\\x03\\x05\' -t')
print('\tdestruktivní odečtení aktuální buňky od buňky následující')
args = 'python brainx.py [>-<-] -m b\'\\x03\\x05\' -t'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/memory07_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

clean()
# #
# # basic brainfuck tests
# #
#
# test 1
print('\n\nTest 1: brainx tests/hello1.b')
print('\tHelloWorld s \\n')
args = 'python brainx.py tests/hello1.b'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b'Hello World!\n'
print( "return code:", p.returncode )
assert p.returncode == 0
print( "error:", error )
# assert error == b''
clean()
# # test 2a
print('\n\nTest 2a: brainx tests/hello2.b')
print('\tHelloWorld bez \\n')
args = 'python brainx.py tests/hello2.b'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
# assert error == b''
clean()
# # test 2b
print('\n\nTest 2b: brainx -t tests/hello2.b')
print('\tHelloWorld bez \\n plus log')
args = 'python brainx.py -t tests/hello2.b'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
# assert error == b''
with open('tests/hello2_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
clean()
# # test 2c
print('\n\nTest 2c: brainx tests/hello2t.b')
print('\tHelloWorld bez \\n plus dva průběžné logy')
args = 'python brainx.py tests/hello2t.b'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/hello2t_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out
with open('tests/hello2t_debug_02.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_02.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

# clean()
#
# brainfuck with input
#
clean()
# test 3
print('\n\nTest 3: brainx tests/numwarp_input.b')
print('\tnumwarp.b pro vstup "123"')
args = 'python brainx.py tests/numwarp_input.b'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output.replace(b'\r', b'') == b'    /\\\n     /\\\n  /\\  /\n   / \n \\ \\/\n  \\\n   \n'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''

clean()
#
# basic PNG
#

# test 4a
print('\n\nTest 4a: brainx tests/sachovnice.jpg')
print('\tumíme jen PNG')
args = 'python brainx.py tests/sachovnice.jpg'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b''
print( "return code:", p.returncode )
# assert p.returncode == 4
#print( "error:", error )
assert b'PNGWrongHeaderError' in error
clean()
# test 4b
print('\n\nTest 4b: brainx tests/sachovnice_paleta.png')
print('\tumíme jen některá PNG')
args = 'python brainx.py tests/sachovnice_paleta.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b''
print( "return code:", p.returncode )
#assert p.returncode == 8
#print( "error:", error )
assert b'PNGNotImplementedError' in error

clean()
#
# brainloller
#
clean()
# test 5a
print('\n\nTest 5a: brainx tests/HelloWorld.png')
print('\tnačtení dat z obrázku HelloWorld.png')
args = 'python brainx.py tests/HelloWorld.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
clean()
# test 5b
print('\n\nTest 5b: brainx -t tests/HelloWorld.png')
print('\tnačtení dat z obrázku HelloWorld.png plus log')
args = 'python brainx.py -t tests/HelloWorld.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b'Hello World!'
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('tests/HelloWorld_debug_01.log', mode='r', encoding='ascii') as f:
    txt_in = f.read()
with open('debug/debug_01.log', mode='r', encoding='ascii') as f:
    txt_out = f.read()
assert txt_in == txt_out

clean()

# everything went OK


# convert tests
clean()
print('\n\nTest 6a: brainx -lc2f tests/HelloWorld.png out.b')
print('\tkonverze brainloller -> brainfuck')
args = 'python brainx.py --lc2f tests/HelloWorld.png out.b'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''
with open('out.b', mode='r', encoding='ascii') as f:
    txt_in = f.read()

assert txt_in == ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+."  # hardcoded, z hello2.b

clean()
print('\n\nTest 6b: brainx --f2lc tests/hello2.b in.png copter.png && brainx --lc2f copter.png out.b')
print('\tkonverze brainfuck -> braincopter -> brainfuck')
args = 'python brainx.py --f2lc -i tests/hello2.b in.png -o copter.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''

args = 'python brainx.py --lc2f copter.png out.b'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
assert output == b''
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
assert error == b''

with open('out.b', mode='r', encoding='ascii') as f:
    txt_in = f.read()

assert txt_in == ">+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+."  # hardcoded, z hello2.b


clean()
print('\n\nTest 6c: brainx --f2lc -i hello2.b -o output.png && brainx output.png')
print('\tkonverze brainfuck-> brainloller, nasledna intepretace ze souboru')
args = 'python brainx.py --f2lc -i tests/hello2.b -o output.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
#assert error == b''
args = 'python brainx.py output.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
print( "return code:", p.returncode )
assert p.returncode == 0
assert output.replace(b'\r', b'').replace(b'\n', b'') == b'Hello World!'
assert error == b''


clean()
print('\n\nTest 6d: brainx --f2lc -i hello2.b in.png -o output.png && brainx output.png')
print('\tkonverze brainfuck-> braincopter, nasledna intepretace ze souboru')
args = 'python brainx.py --f2lc -i tests/hello2.b in.png -o output.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
print( "return code:", p.returncode )
assert p.returncode == 0
#print( "error:", error )
#assert error == b''
args = 'python brainx.py output.png'
p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = p.communicate()
print( "output:", output )
print( "return code:", p.returncode )
assert p.returncode == 0
assert output.replace(b'\r', b'').replace(b'\n', b'') == b'Hello World!'
assert error == b''

print('\n\n', '-'*70, '\n', 'OK: All tests passed.')
