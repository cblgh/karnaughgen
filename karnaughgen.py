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

import itertools
import math
import sys

from PySide import QtCore, QtGui


class MainFrame(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(500, 350)
        self.move(50, 50)
        self.setWindowTitle('KarnaughLaTeX generator')
        self._hbox = QtGui.QHBoxLayout()
        self._hbox.setContentsMargins(0, 0, 0, 0)
        # A list of all stored cubes.
        self._cubes = []
        # Karnaugh map
        self._karnaugh_map = KarnaughMap(4)
        self._hbox.addWidget(self._karnaugh_map)
        # Implicant list
        self._implicant_list = ImplicantList(self._cubes)
        self._hbox.addWidget(self._implicant_list, QtCore.Qt.AlignRight)
        # Add implicant-button
        self._vbox = QtGui.QVBoxLayout()
        self._add_button = QtGui.QPushButton('Add implicant')
        self._add_button.clicked.connect(self._add_implicant)
        self._vbox.addLayout(self._hbox, 1)
        self._vbox.addWidget(self._add_button)
        # Generate LaTeX-code-button
        self._generate_latex_button = QtGui.QPushButton('Generate LaTeX')
        self._generate_latex_button.clicked.connect(self._generate_latex)
        self._vbox.addWidget(self._generate_latex_button)
        # Cannot set layout on QMainWindow, so placeholder widget must be made.
        layout_widget = QtGui.QWidget()
        layout_widget.setLayout(self._vbox)
        self.setCentralWidget(layout_widget)

    def _add_implicant(self):
        # Fetch current selection, validate it, convert to a cube ({0, 1, B})
        vertices = self._karnaugh_map.selected_vertices()
        if len(vertices) > 0:
            cube = self._validate_selection(vertices)
            # Add cube to implicant list.
            self._cubes.append(cube)
            self._implicant_list.refresh_cubes()

    def _generate_latex(self):
        """Takes all implicants and generates LaTeX code in a new dialog."""
        self._dialog = LaTeXGeneratorDialog(self._cubes)
        self._dialog.show()

    def _validate_selection(self, vertices):
        def is_power_of_two(num):
            return num != 0 and (num & (num - 1)) == 0
        # Check total item count. Must be a power of 2.
        if not is_power_of_two(len(vertices)):
            raise Exception("Total count not power of 2, was", len(vertices))
        # Ensures that selection is a rectangle with element count that is 2^x.
        return self._vertices_to_cube(vertices)

    def _vertices_to_cube(self, vertices):
        """Convert the list of vertices to a cube.

        Throw an exception if the calculated cube has a size that does not
        equal the coordinate count. This may happen if the input vertices
        is not a rectangular area in the Karnaugh map.
        """
        def lattice(var):
            if all(i == '1' for i in var):
                return '1'
            elif all(i == '0' for i in var):
                return '0'
            else:
                return 'B'
        cube = ''.join(lattice(var) for var in zip(*vertices))
        # Now ensure that the generated cube has size equal to the vertex count
        if 2 ** cube.count('B') != len(vertices):
            raise Exception("Invalid implicant selection for cube", cube)
        return cube


class KarnaughMap(QtGui.QTableWidget):

    ROW_HEIGHT = 50

    def __init__(self, variables):
        if variables > 4 or variables < 2:
            raise Exception('Illegal variable count. Must be between 2 and 4.')
        left_vars = (variables // 2) * 2
        top_vars = math.ceil(variables / 2) * 2
        # Create table view with correct row and column count.
        super().__init__(left_vars, top_vars)
        self._set_headers(left_vars, top_vars)
        # Create cells, and set cell width equal to cell height for all cells.
        indices = itertools.product(range(0, left_vars), range(0, top_vars))
        for r, c in indices:
            item = QtGui.QTableWidgetItem('0')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setItem(r, c, item)
        for row in range(0, left_vars):
            self.setRowHeight(row, self.ROW_HEIGHT)
        for col in range(0, top_vars):
            self.setColumnWidth(col, self.rowHeight(0))

    def selected_vertices(self):
        """Returns a set of vertices of the selected items."""
        coords = ((i.row(), i.column()) for i in self.selectedIndexes())
        return [self._left_values[r] + self._top_values[c] for r, c in coords]

    def _set_headers(self, left_vars, top_vars):
        # left_vars and top_vars will only be 2 or 4.
        two_var = ['0', '1']
        four_var = ['00', '01', '11', '10']
        self._left_values = two_var if left_vars == 2 else four_var
        self._top_values = two_var if top_vars == 2 else four_var
        self.setVerticalHeaderLabels(self._left_values)
        self.setHorizontalHeaderLabels(self._top_values)


class ImplicantList(QtGui.QListWidget):

    VARIABLES = ['x1', 'x2', 'x3', 'x4']

    def __init__(self, cubes):
        super().__init__()
        self._cubes = cubes

    def refresh_cubes(self):
        """Show all implicants of the cube list in this QListWidget."""
        def variable(pos, value):
            """Returns the variable as used in disjunctive form."""
            if value == '0':
                return self.VARIABLES[pos] + "'"
            elif value == '1':
                return self.VARIABLES[pos]
            else:
                return ''

        def expr(cube):
            return ''.join(variable(i, v) for i, v in enumerate(cube))
        items = [expr(c) for c in self._cubes]
        self.clear()
        self.addItems(items)


class LaTeXGenerator(object):

    @staticmethod
    def generate(cubes):
        """Return the generated LaTeX code for the given cubes."""
        # Ensure that all cubes have identical amount of variables, and that
        # the number of cubes is larger than 0.
        if not len({len(c) for c in cubes}) == 1:
            raise Exception("Invalid input cubes.")
        # Try to locate a B0-sequence in the left-hand side variables.
        code = (LaTeXGenerator.generate_cube(c) for c in cubes)
        return '\n'.join(code)

    @staticmethod
    def generate_cube(cube):
        # Hard-code the special cases, that is the cases where we need to
        # generate implicants going "over the edge".
        # After checking for every weird case, just use general code to create
        # a regular implicant (that is, a rectangle in the middle of the
        # Karnaugh map)

        # Assume there are 4 variables, x1x2 on the left-hand side, x3x4 on top
        # We wrap around the edge as soon as any variable pair is B0.
        # Example: 00B0 wrap left-right
        # Example: B011 wrap top-bottom.
        # Example: B0B0 wrap top-bottom and left-right.
        # If there are 3 variables, assume x1 is the single left-hand variable
        # This means that there cannot be any top-bottom wraps in this case.
        # If there are 2 variables, no wraps can occur.
        def coord(onetwovars):
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
            # \PrimImpl(x,y)(w,h)[rlbt]
            IMPL = '\\PrimImpl({:d},{:d})({:d},{:d})'
            v = IMPL.format(x, y, width - 2, height - 2, mod)
            return v if mod == '' else '{}[{}]'.format(v, mod)

        variables = len(cube)
        code = []
        leftvars = cube[:variables//2]
        topvars = cube[-variables//2:]
        if variables == 4 and cube == 'B0B0':
            # Special case, mark the four corners. Hard coded...
            width = 30
            height = 30
            x_left = 5
            x_right = 55
            y_bottom = -5
            y_top = 45
            code.append(impl(x_left, y_top, width, height, 'rb'))
            code.append(impl(x_right, y_top, width, height, 'lb'))
            code.append(impl(x_left, y_bottom, width, height, 'rt'))
            code.append(impl(x_right, y_bottom, width, height, 'lt'))
        elif variables == 4 and leftvars == 'B0':
            # Wrap top-bottom. Height will always be 20+10 for 3/4-vars + wrap.
            width = (2 ** topvars.count('B')) * 10
            height = 30
            x = 10 + coord(topvars) + width//2
            y_top = 45
            y_bottom = -5
            code.append(impl(x, y_top, width, height, 'b'))
            code.append(impl(x, y_bottom, width, height, 't'))
        elif variables >= 3 and topvars == 'B0':
            # Wrap left-right.
            width = 30
            height = (2 ** leftvars.count('B')) * 10
            x_left = 5
            x_right = 55
            y = 40 - coord(leftvars) - height//2
            code.append(impl(x_left, y, width, height, 'r'))
            code.append(impl(x_right, y, width, height, 'l'))
        else:
            # Ordinary cases here, no wraps at all, so just calculate as usual.
            width = (2 ** topvars.count('B')) * 10
            height = (2 ** leftvars.count('B')) * 10
            x = 10 + coord(topvars) + width//2
            y = 40 - coord(leftvars) - height//2
            code.append(impl(x, y, width, height))
        return '\n'.join(code)


class LaTeXGeneratorDialog(QtGui.QWidget):

    def __init__(self, cubes):
        super().__init__()
        self.resize(400, 200)
        self.move(100, 100)
        font = QtGui.QFont("")
        font.setStyleHint(QtGui.QFont.TypeWriter)
        self.setFont(font)
        text = LaTeXGenerator.generate(cubes)
        text_edit = QtGui.QTextEdit()
        text_edit.setPlainText(text)
        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(text_edit)
        self.setLayout(vbox)


def main():
    app = QtGui.QApplication(sys.argv)
    main_frame = MainFrame()
    main_frame.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
