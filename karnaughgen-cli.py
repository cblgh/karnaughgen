#!/usr/bin/env python3

# Copyright (c) 2013, Linus Karlsson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of Linus Karlsson nor the names of the contributors may
#    be used to endorse or promote products derived from this software without
#    specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import re

import karnaughgen


def cube_parse(s):
    """Takes an input string and ensures that it is a valid cube."""
    if re.match('^[01B]{2,4}$', s) is not None:
        return s
    else:
        raise argparse.ArgumentTypeError('{} is not a valid cube'.format(s))


def parse_arguments():
    """Parses arguments and return a tuple of (function values, cubes)."""
    parser = argparse.ArgumentParser(
        description='Generates LaTeX code for Karnaugh maps.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='examples:\n'
        '  %(prog)s B001\n'
        '  %(prog)s -v=-1-11-1-00000001 0BBB B111')
    parser.add_argument('-v', '--values', action='store',
                        help='The values of the function f. Expected input is '
                        'a string of length 4, 8, or 16, corresponding to the '
                        'number of variables (2, 3, or 4). The function values'
                        ' should be in natural order. Defaults to all zero. '
                        "To pass don't care terms, use the syntax "
                        '--values=-1-1 (note the equal sign (=)) to avoid '
                        'the parser to interpret it as an option.')
    parser.add_argument('cubes', metavar='CUBE', type=cube_parse, nargs='+',
                        help='A space-separated list of cubes for each '
                        'implicant that should be included in the output. '
                        'A cube is a string of 2-4 chars from the set '
                        '{0, 1, B}. Examples: 0B01, BB10, B10, 0B.')
    args = parser.parse_args()
    # Now, ensure that the number of variables in all cubes match.
    if len({len(c) for c in args.cubes}) != 1:
        parser.error('all cubes must contain the same variable count.')
    variables = len(args.cubes[0])
    # Also ensure that the length of the (optional) values string matches the
    # variable count of the cubes.
    default_values = '0' * (2**variables)
    values = args.values if args.values is not None else default_values
    if 2 ** variables != len(values):
        parser.error("function values length must match cube's variable count")
    # Alles gut.
    return values, args.cubes


def main():
    values, cubes = parse_arguments()
    try:
        latex = karnaughgen.LaTeXGenerator.generate(cubes, values)
        print(latex)
    except karnaughgen.KarnaughError as e:
        print("error:", e)

if __name__ == '__main__':
    main()
