#!/usr/bin/env python3
# number sequence puzzle generator
# Copyright (C) 2020 by Arjen Lentz
# Licensed under AGPLv3

# 2020-02-01 initial stuffs

import sys
import random


capability_operations = [ 'add',
                            'subtract',
                            'multiply',
                            'add-previous', 
                            'addself',
                            'addself-add',
                            'add-multiply',
                            'subtract-multiply',
                            'multiply-add',
                            'multiply-subtract',
                            'multiply-self'
                            ]



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


# initialise pseudo-random generator
random.seed()


# init start [0] value of sequence
sequence = [ random.randint(1,10) ]
change_value1 = random.randint(1,10)
change_value2 = random.randint(1,10)
# pick operation
operation = random.choice(capability_operations)
# 
if (operation == 'add-previous'):
    sequence.append(change_value2)
    for i in range (1, 3):
        sequence.append(do_operation2(sequence[i - 1], sequence[i], operation))
else:
    for i in range (0, 3):
        sequence.append(do_operation(sequence[i], operation, change_value1, change_value2))

# debug output to stderr (redirect with 2>>pathname)
# bit crude as change_value2 (and even change_value1) not always used
print(operation, change_value1, change_value2, file=sys.stderr)
# regular output to stdout (redirect with >>pathname)
for x in sequence:
    print(x, end=', ')
print('...')

# eof