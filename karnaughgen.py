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


class KarnaughError(Exception):
    pass


class LaTeXGenerator(object):

    @staticmethod
    def generate(cubes, values):
        """Return the generated LaTeX code for the given cubes."""
        # Ensure that all cubes have identical amount of variables, and that
        # the number of cubes is larger than 0. Also ensure that the length
        # of values matches the amount of variable combinations.
        if not len({len(c) for c in cubes}) == 1:
            raise KarnaughError("Invalid input cubes.")
        if not 2 ** len(cubes[0]) == len(values):
            raise KarnaughError("Invalid length of input values.")
        implicants = '\n'.join(LaTeXGenerator.generate_cube(c) for c in cubes)
        variables = len(cubes[0])
        valstr = ''.join(values)
        return '\n'.join([LaTeXGenerator.generate_header(variables, valstr),
                          implicants,
                          LaTeXGenerator.generate_footer()])

    @staticmethod
    def generate_cube(cube):
        # Assume there are 4 variables, x1x2 on the left-hand side, x3x4 on top
        # We wrap around the edge as soon as any variable pair is B0.
        # Example: 00B0 wrap left-right
        # Example: B011 wrap top-bottom.
        # Example: B0B0 wrap top-bottom and left-right.
        # If there are 3 variables, assume x1 is the single left-hand variable
        # This means that there cannot be any top-bottom wraps in this case.
        # If there are 2 variables, no wraps can occur.
        def coord(onetwovars):
            """Maps the 1-2 left or 1-2 top variables to coordinate."""
            m = {'00': 0,
                 '01': 1,
                 '11': 2,
                 '10': 3,
                 '0B': 0,
                 '1B': 2,
                 'B1': 1,
                 'BB': 0}
            return m['{:0>2}'.format(onetwovars)] * 10

        def impl(x, y, width, height, mod=''):
            """Returns a LaTeX prime implicant as \\PrimImpl(x,y)(w,h)[rlbt]"""
            IMPL = '\\PrimImpl({:d},{:d})({:d},{:d})'
            v = IMPL.format(x, y, width - 2, height - 2)
            return v if mod == '' else '{}[{}]'.format(v, mod)

        variables = len(cube)
        leftvars = cube[:variables//2]
        topvars = cube[-variables//2:]

        def xcoord(width):
            """Returns x-coordinate, origin is bottom-left."""
            return 10 + coord(topvars) + width//2

        def ycoord(height):
            """Returns y-coordinate, origin is bottom-left."""
            return (2**len(leftvars))*10 - coord(leftvars) - height//2

        code = []
        # These height and width will require 10 extra px if they are wrapped.
        width = (2 ** topvars.count('B')) * 10
        height = (2 ** leftvars.count('B')) * 10
        # Constant coordinates used in wraps.
        x_left, x_right, y_bottom, y_top = 5, 55, -5, 45
        if variables == 4 and cube == 'B0B0':
            # Special case, mark the four corners.
            code.append(impl(x_left, y_top, width + 10, height + 10, 'rb'))
            code.append(impl(x_right, y_top, width + 10, height + 10, 'lb'))
            code.append(impl(x_left, y_bottom, width + 10, height + 10, 'rt'))
            code.append(impl(x_right, y_bottom, width + 10, height + 10, 'lt'))
        elif variables == 4 and leftvars == 'B0':
            # Wrap top-bottom.
            code.append(impl(xcoord(width), y_top, width, height + 10, 'b'))
            code.append(impl(xcoord(width), y_bottom, width, height + 10, 't'))
        elif variables >= 3 and topvars == 'B0':
            # Wrap left-right.
            code.append(impl(x_left, ycoord(height), width + 10, height, 'r'))
            code.append(impl(x_right, ycoord(height), width + 10, height, 'l'))
        else:
            # Ordinary cases here, no wraps.
            code.append(impl(xcoord(width), ycoord(height), width, height))
        return '\n'.join(code)

    def generate_footer():
        return '}\n\\end{picture}\n'

    def generate_header(variables, values, ):
        HEADER = ('\\begin{{picture}}(60,60)(0,0)\n'
                  '\\put(0,10){{\n'
                  '\\Karnaughdiagram{{{:d}}}{{{}}}(${}$, ${}$)[${}$]')
        VARS = ['x_1', 'x_2', 'x_3', 'x_4']
        left_vars = ' '.join(VARS[:variables//2])
        top_vars = ' '.join(VARS[variables//2:variables])
        func = 'f'
        return HEADER.format(variables, values, left_vars, top_vars, func)
