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

if __name__ == '__main__':
    unittest.main()
