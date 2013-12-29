karnaughgen
===========

Generates LaTeX-code for Karnaugh maps using a GUI.

Requirements
------------

 *  Python 2 or 3
 *  The generated LaTeX-code requires Karnaugh.sty to be compiled to a document.

### GUI-version

 *  Python 3 only
 *  PySide

Usage
-----
### GUI-version
```
python3 karnaughgen-gui.py
```

### CLI-version
```
usage: karnaughgen-cli.py [-h] [-v VALUES] CUBE [CUBE ...]

Generates LaTeX code for Karnaugh maps.

positional arguments:
  CUBE                  A space-separated list of cubes for each implicant
                        that should be included in the output. A cube is a
                        string of 2-4 chars from the set {0, 1, B}. Examples:
                        0B01, BB10, B10, 0B.

optional arguments:
  -h, --help            show this help message and exit
  -v VALUES, --values VALUES
                        The values of the function f. Expected input is a
                        string of length 4, 8, or 16, corresponding to the
                        number of variables (2, 3, or 4). The function values
                        should be in natural order. Defaults to all zero. To
                        pass don't care terms, use the syntax --values=-1-1
                        (note the equal sign (=)) to avoid the parser to
                        interpret it as an option.

examples:
  karnaughgen-cli.py B001
  karnaughgen-cli.py -v=-1-11-1-00000001 0BBB B111
```

Licence
-------

```
Copyright (c) 2013, Linus Karlsson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

 * Neither the name of Linus Karlsson nor the names of the contributors may
   be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGE.
```
