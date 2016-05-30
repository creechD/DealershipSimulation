#Interphase - Pygame Interface Module
#Copyright (c) 2009 James Garnon
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.
#
#Interphase version 0.87
#Project Site: http://gatc.ca/

try:
    import pygame as engine
except ImportError:
    engine = None


initialized = False


def get_init():
    """
    Check if module is initialized.
    """
    return initialized


def _init(engine):
    global Interface, EVENT, Control, FunctionControl, Label, Textbox, Text, load_image, __version__, initialized
    import env
    env.engine = engine
    from interface import Interface, EVENT
    from control import Control, FunctionControl, Label, Textbox
    from util import Text, load_image
    from version import __version__
    initialized = True


def init(engine):
    """
    Initialize module. Argument engine is the multimedia framework object.
    Engine can be Pygame, PyJ2D, or Pyjsdl.
    Module initialized if Pygame can be imported.
    """
    if initialized:
        return
    _init(engine)
    if engine.__name__ == 'pyjsdl':
        from image import _load_default_images
        _load_default_images()


if engine:
    _init(engine)

