#!/usr/bin/env python3

import time, random

symbols = '▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟ '

# Line of symbols: repeatedly replace the whole line of symbols.
def glitch_line1():
    while True:
        print(''.join(random.choices(symbols, k=50)), end='\r')
        time.sleep(0.1)

# Line of symbols: repeatedly replace a random symbol.
def glitch_line2():
    lst = random.choices(symbols, k=50)
    while True:
        lst[random.randrange(len(lst))] = random.choice(symbols)
        print(''.join(lst), end='\r')
        time.sleep(0.01)

# Line of symbols; replace symbols in a swiping motion.
def glitch_line3():
    i = 0
    while True:
        print(random.choice(symbols), end='', flush=True)
        if i == 0: print('\r', end='')
        i = (i + 1) % 50
        time.sleep(0.01)

glitch_line2()
