#!/usr/bin/env python3
# number sequence puzzle generator
# Copyright (C) 2020 by Arjen Lentz
# Licensed under AGPLv3

# 2020-02-01 initial stuffs

import sys
import random
import argparse


def do_operation (current_value, operation, change_value1, change_value2):
    return {
        'add': current_value + change_value1,
        'subtract': current_value - change_value1,
        'multiply': current_value * change_value1,
        'addself': current_value * 2,
        'addself-add': (current_value * 2) + change_value1,
        'add-multiply': (current_value + change_value1) * change_value2,
        'subtract-multiply': (current_value - change_value1) * change_value2,
        'multiply-add': (current_value * change_value1) + change_value2,
        'multiply-subtract': (current_value * change_value1) - change_value2,
        'multiply-self': current_value * current_value,
    }[operation]


def do_operation2 (previous_value, current_value, operation):
    return {
        'add-previous': current_value + previous_value,
    }[operation]


# command line options and usage info
parser = argparse.ArgumentParser(description = 'Generate number sequence puzzles')
parser.add_argument('--count', type=int, default=1, help='How many sequences to generate')
parser.add_argument('--start', type=int, default=10, help="Upper limit of start value (default: %(default)s)")
parser.add_argument('--limit1', type=int, default=10, help="Upper limit of 1st change value (default: %(default)s)")
parser.add_argument('--limit2', type=int, default=10, help="Upper limit of 2st change value (default: %(default)s)")
parser.add_argument('--debug', action='store_true', help='Show pattern rule')
parser.add_argument('level', choices=['basic', 'two-step'], help='Complexity level')


args = parser.parse_args()


# basic
capability_operations = [ 'add',
                            'subtract',
                            'multiply',
                            'add-previous'
]

if (args.level == 'two-step'):
   capability_operations.append('addself')
   capability_operations.append('addself-add')
   capability_operations.append('add-multiply')
   capability_operations.append('subtract-multiply')
   capability_operations.append('multiply-add')
   capability_operations.append('multiply-subtract')
   capability_operations.append('multiply-self')


# initialise pseudo-random generator
random.seed()

for n in range(args.count):
    # init start [0] value of sequence
    sequence = [ random.randint(1,args.start) ]
    change_value1 = random.randint(1,args.limit1)
    change_value2 = random.randint(1,args.limit2)
    # pick operation
    operation = random.choice(capability_operations)

    if (operation == 'add-previous'):
        sequence.append(change_value2)
        for i in range (1, 3):
            sequence.append(do_operation2(sequence[i - 1], sequence[i], operation))
    else:
        for i in range (0, 3):
            sequence.append(do_operation(sequence[i], operation, change_value1, change_value2))

    # bit crude as change_value2 (and even change_value1) not always used
    if (args.debug == True):
        print(operation, change_value1, change_value2, end=': ')

    for x in sequence:
        print(x, end=', ')
    print('...')

# eof