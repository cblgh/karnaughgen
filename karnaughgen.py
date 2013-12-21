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

from PyQt4 import QtCore, QtGui


class MainFrame(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(500, 300)
        self.move(50, 50)
        self.setWindowTitle('KarnaughLaTeX generator')
        self._hbox = QtGui.QHBoxLayout()
        self._hbox.setContentsMargins(0, 0, 0, 0)
        # Karnaugh map
        self._karnaugh_map = KarnaughMap(4)
        self._hbox.addWidget(self._karnaugh_map)
        # Implicant list
        self._implicant_list = ImplicantList()
        self._hbox.addWidget(self._implicant_list, QtCore.Qt.AlignRight)
        # Add implicant-button
        self._vbox = QtGui.QVBoxLayout()
        self._add_button = QtGui.QPushButton('Add implicant')
        self._add_button.clicked.connect(self._add_implicant)
        self._vbox.addLayout(self._hbox, 1)
        self._vbox.addWidget(self._add_button)
        # Cannot set layout on QMainWindow, so placeholder widget must be made.
        layout_widget = QtGui.QWidget()
        layout_widget.setLayout(self._vbox)
        self.setCentralWidget(layout_widget)

    def _add_implicant(self):
        # Fetch current selection, validate it, convert to a cube ({0, 1, B})
        vertices = self._karnaugh_map.selected_vertices()
        cube = self._validate_selection(vertices)
        # Add cube to implicant list.
        self._implicant_list.addItem(cube)

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

    def __init__(self):
        super().__init__()


def main():
    app = QtGui.QApplication(sys.argv)
    main_frame = MainFrame()
    main_frame.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
