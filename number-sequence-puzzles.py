#!/usr/bin/env python3
#    number sequence puzzle generator
#    Copyright (C) 2020 by Arjen Lentz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#        https://www.gnu.org/licenses/agpl.txt


# 2020-02-01 initial stuffs
# 2020-02-02 make it more classy
# 2023-01-26 published because why not

import sys
import random
import argparse


class sequence_base():
    def __init__(self):
        self.sequence = [ self.random('start') ]

    def name(self):
        raise Exception('sequence name method not defined')

    def uses_twostep(self):
        return False

    def uses_previous(self):
        return False

    def uses_adaptive(self):
        return False

    def random(self, valref, multiply=False):
        if (valref == 'start'):
            lower = 1
            upper = args.start
        else:
            if (valref == 'value1'):
                upper = args.limit1
            elif (valref == 'value2'):
                upper = args.limit2
            else:
                raise Exception('Unknown random valref')

            if (args.allow_negative_multiplication and multiply):
                lower = -upper
            elif (multiply):
                lower = 2
            else:
                lower = 1

        while True:
            x = random.randint(lower, upper)
            if (x == 0):    # 0 is useless either for addition or multiplication
                continue
            if (x != 1 or not multiply):
                break

        return (x)

    def do_operation(self, i):
        raise Exception('Missing do_operation method')

    def run(self):
        raise Exception('Missing run method')

    def debug(self):
        raise Exception('Missing debug method')


class sequence_add(sequence_base):
    def name(self):
        return 'add'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1')

    def do_operation(self, i):
        return self.sequence[i] + self.change_value1

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = current + {}".format(self.do_operation(args.sequence_length - 1), self.change_value1))


class sequence_subtract(sequence_base):
    def name(self):
        return 'subtract'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1')

    def do_operation(self, i):
        return self.sequence[i] - self.change_value1

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = current - {}".format(self.do_operation(args.sequence_length - 1), self.change_value1))


class sequence_multiply(sequence_base):
    def name(self):
        return 'multiply'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1', multiply=True)

    def do_operation(self, i):
        return self.sequence[i] * self.change_value1

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = current * {}".format(self.do_operation(args.sequence_length - 1), self.change_value1))


class sequence_addprevious(sequence_base):
    def name(self):
        return 'addprevious'

    def __init__(self):
        super().__init__()
        self.sequence.append(self.random('value1'))

    def uses_previous(self):
        return True

    def do_operation(self, i):
        return self.sequence[i] + self.sequence[i - 1]

    def run(self):
        for i in range(1, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = current + previous".format(self.do_operation(args.sequence_length - 1)))


class sequence_multiplyself(sequence_base):
    def name(self):
        return 'multiplyself'

    def do_operation(self, i):
        return self.sequence[i] * self.sequence[i]

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = current * current".format(self.do_operation(args.sequence_length - 1)))


class sequence_add_xadd(sequence_base):
    def name(self):
        return 'add_xadd'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1')
        self.change_value2 = self.random('value2')

    def uses_adaptive(self):
        return True

    def do_operation(self, i):
        return self.sequence[i] + self.change_value1

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
            # we have to do the xadd here, otherwise debug will show the wrong value
            self.change_value1 += self.change_value2
        return self.sequence

    def debug(self):
        print(" {}, change = {}, next = current + change, change = change + {}".format(self.do_operation(args.sequence_length - 1), self.change_value1, self.change_value2))


class sequence_add_multiply(sequence_base):
    def name(self):
        return 'add_multiply'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1')
        self.change_value2 = self.random('value2', multiply=True)

    def uses_twostep(self):
        return True

    def do_operation(self, i):
        return (self.sequence[i] + self.change_value1) * self.change_value2

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = (current + {}) * {}".format(self.do_operation(args.sequence_length - 1), self.change_value1, self.change_value2))


class sequence_subtract_multiply(sequence_base):
    def name(self):
        return 'subtract_multiply'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1')
        self.change_value2 = self.random('value2', multiply=True)

    def uses_twostep(self):
        return True

    def do_operation(self, i):
        return (self.sequence[i] - self.change_value1) * self.change_value2

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = (current - {}) * {}".format(self.do_operation(args.sequence_length - 1), self.change_value1, self.change_value2))


class sequence_multiply_add(sequence_base):
    def name(self):
        return 'multiply_add'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1', multiply=True)
        self.change_value2 = self.random('value2')

    def uses_twostep(self):
        return True

    def do_operation(self, i):
        return (self.sequence[i] * self.change_value1) + self.change_value2

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = (current * {}) + {}".format(self.do_operation(args.sequence_length - 1), self.change_value1, self.change_value2))


class sequence_multiply_subtract(sequence_base):
    def name(self):
        return 'multiply_subtract'

    def __init__(self):
        super().__init__()
        self.change_value1 = self.random('value1', multiply=True)
        self.change_value2 = self.random('value2')

    def uses_twostep(self):
        return True

    def do_operation(self, i):
        return (self.sequence[i] * self.change_value1) - self.change_value2

    def run(self):
        for i in range(0, args.sequence_length - 1):
            self.sequence.append(self.do_operation(i))
        return self.sequence

    def debug(self):
        print(" {}, next = (current * {}) - {}".format(self.do_operation(args.sequence_length - 1), self.change_value1, self.change_value2))


def select_operation (operation):
    return {
        'add': sequence_add(),
        'subtract': sequence_subtract(),
        'multiply': sequence_multiply(),
        'addprevious': sequence_addprevious(),
        'multiplyself': sequence_multiplyself(),
        'add_xadd': sequence_add_xadd(),
        'add_multiply': sequence_add_multiply(),
        'subtract_multiply': sequence_subtract_multiply(),
        'multiply_add': sequence_multiply_add(),
        'multiply_subtract': sequence_multiply_subtract(),
    }[operation]



# check a calculated sequence for some possibly undesirable situations
def check_sequence(op):
    prev = 0
    dups = -1
    for x in op.sequence:
        # do we allow negative values in the output sequence?
        if (x < 0 and args.allow_negative_sequence is False):
            return False
        # do we allow values this large in our sequence?
        if (args.sequence_limit and abs(x) > args.sequence_limit):
            return False
        # check if more than 2 sequence values are the same
        # we can have all the same or end up at 0 early on
        if (dups >= 0 and x == prev):
            dups += 1
        else:
            prev = x
            dups = 0

    if (dups >= 2):
        return False
    return True


# command line options and usage info
parser = argparse.ArgumentParser(description = 'Generate number sequence puzzles')
parser.add_argument('count', type=int, default=1, help='How many sequences to generate')
parser.add_argument('--start', type=int, default=10, help="Upper limit of start value (default: %(default)s)")
parser.add_argument('--limit1', type=int, default=10, help="Upper limit of 1st change value (default: %(default)s)")
parser.add_argument('--limit2', type=int, default=10, help="Upper limit of 2st change value (default: %(default)s)")
parser.add_argument('--sequence-length', type=int, default=4, choices=range(4,11), help="How many values to show in sequence (range: 4-10, default: %(default)s)")
parser.add_argument('--sequence-limit', type=int, default=0, help="Set upper limit on sequence values (default: none)")
parser.add_argument('--allow-twostep', action='store_true', help='Allow two-step operations')
parser.add_argument('--allow-previous', action='store_true', help='Allow operations involving previous value in sequence')
parser.add_argument('--allow-adaptive', action='store_true', help='Allow change value to be subject to a change constant')
parser.add_argument('--allow-negative-multiplication', action='store_true', help='Allow multiplication change values to be negative (also enables allow-negative-sequence)')
parser.add_argument('--allow-negative-sequence', action='store_true', help='Allow sequence values to be negative')
parser.add_argument('--allow-complex', action='store_true', help='Enable all allow options for maximum complexity')
parser.add_argument('--debug', action='store_true', help='Show next value in sequence, and pattern rule')


args = parser.parse_args()
if (args.allow_complex):
    args.allow_twostep = args.allow_previous = args.allow_adaptive = args.allow_negative_multiplication = args.allow_negative_sequence = True
if (args.allow_negative_multiplication):
    args.allow_negative_sequence = True

def check_new_operation(capability_operations, method):
    if ((not method.uses_twostep(method) or args.allow_twostep) and
        (not method.uses_previous(method) or args.allow_previous) and
        (not method.uses_adaptive(method) or args.allow_adaptive)):
        capability_operations.append(method.name(method))


capability_operations = []
check_new_operation(capability_operations, sequence_add)
check_new_operation(capability_operations, sequence_subtract)
check_new_operation(capability_operations, sequence_multiply)
check_new_operation(capability_operations, sequence_addprevious)

check_new_operation(capability_operations, sequence_add_xadd)

check_new_operation(capability_operations, sequence_add_multiply)
check_new_operation(capability_operations, sequence_subtract_multiply)
check_new_operation(capability_operations, sequence_multiply_add)
check_new_operation(capability_operations, sequence_multiply_subtract)
check_new_operation(capability_operations, sequence_multiplyself)

if (args.debug):
    print("Options:", args)
    print("Configured for the following operations:", capability_operations)


# initialise pseudo-random generator
random.seed()

for n in range(args.count):
    while True:
        # pick operation
        # we pick a new operation on looping as otherwise we could get stuck
        # e.g. with a low upper sequence limit and self-multiplication
        operation = random.choice(capability_operations)

        op = select_operation(operation)
        op.run()

        if check_sequence(op):
            break
        # loop to try again

    for x in op.sequence:
        print(x, end=', ')
    print('...', end='')

    if (args.debug is True):
        op.debug()

    print()

# eof
