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

import karnaughgen
import unittest


class TestLaTeXGenerator(unittest.TestCase):

    def test_B000(self):
        i = 'B000'
        expected = ("\\PrimImpl(15,45)(8,28)[b]\n"
                    "\\PrimImpl(15,-5)(8,28)[t]")
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_0BB0(self):
        i = '0BB0'
        expected = ("\\PrimImpl(5,30)(28,18)[r]\n"
                    "\\PrimImpl(55,30)(28,18)[l]")
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_B0B0(self):
        i = 'B0B0'
        expected = ("\\PrimImpl(5,45)(28,28)[rb]\n"
                    "\\PrimImpl(55,45)(28,28)[lb]\n"
                    "\\PrimImpl(5,-5)(28,28)[rt]\n"
                    "\\PrimImpl(55,-5)(28,28)[lt]")
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_B010(self):
        i = 'B010'
        expected = ("\\PrimImpl(45,45)(8,28)[b]\n"
                    "\\PrimImpl(45,-5)(8,28)[t]")
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_B01B(self):
        i = 'B01B'
        expected = ("\\PrimImpl(40,45)(18,28)[b]\n"
                    "\\PrimImpl(40,-5)(18,28)[t]")
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_0B0B(self):
        i = '0B0B'
        expected = "\\PrimImpl(20,30)(18,18)"
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_B1B1(self):
        i = 'B1B1'
        expected = "\\PrimImpl(30,20)(18,18)"
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_BB1B(self):
        i = 'BB1B'
        expected = "\\PrimImpl(40,20)(18,38)"
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_1111(self):
        i = '1111'
        expected = "\\PrimImpl(35,15)(8,8)"
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_111(self):
        i = '111'
        expected = '\\PrimImpl(35,5)(8,8)'
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_BB1(self):
        i = 'BB1'
        expected = '\\PrimImpl(30,10)(18,18)'
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_1B0(self):
        i = '1B0'
        expected = ('\\PrimImpl(5,5)(28,8)[r]\n'
                    '\\PrimImpl(55,5)(28,8)[l]')
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_10(self):
        i = '10'
        expected = '\\PrimImpl(15,5)(8,8)'
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_BB(self):
        i = 'BB'
        expected = '\\PrimImpl(20,10)(18,18)'
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate_cube(i))

    def test_latex_generator_4var(self):
        i = (['BB1B', 'B01B'], '0000000000000000')
        expected = ('\\begin{picture}(60,60)(0,0)\n'
                    '\\put(0,10){\n'
                    '\\Karnaughdiagram{4}{0000000000000000}'
                    '($x_1 x_2$, $x_3 x_4$)[$f$]\n'
                    '\\PrimImpl(40,20)(18,38)\n'
                    '\\PrimImpl(40,45)(18,28)[b]\n'
                    '\\PrimImpl(40,-5)(18,28)[t]\n'
                    '}\n'
                    '\\end{picture}\n')
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate(*i))

    def test_latex_generator_3var(self):
        i = (['BB1', '1B0'], '00000000')
        expected = ('\\begin{picture}(60,60)(0,0)\n'
                    '\\put(0,10){\n'
                    '\\Karnaughdiagram{3}{00000000}'
                    '($x_1$, $x_2 x_3$)[$f$]\n'
                    '\\PrimImpl(30,10)(18,18)\n'
                    '\\PrimImpl(5,5)(28,8)[r]\n'
                    '\\PrimImpl(55,5)(28,8)[l]\n'
                    '}\n'
                    '\\end{picture}\n')
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate(*i))

    def test_latex_generator_2var(self):
        i = (['BB', '01'], '0000')
        expected = ('\\begin{picture}(60,60)(0,0)\n'
                    '\\put(0,10){\n'
                    '\\Karnaughdiagram{2}{0000}'
                    '($x_1$, $x_2$)[$f$]\n'
                    '\\PrimImpl(20,10)(18,18)\n'
                    '\\PrimImpl(25,15)(8,8)\n'
                    '}\n'
                    '\\end{picture}\n')
        self.assertEqual(expected, karnaughgen.LaTeXGenerator.generate(*i))

if __name__ == '__main__':
    unittest.main()
