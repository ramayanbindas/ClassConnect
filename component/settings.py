'''
# version: 1.0.0
:about: This module contains all the necessary constants, settings need for the
application,

'''

from os.path import abspath

# if the application runs over the window.
BASEFILEPATH = abspath(__file__).removesuffix("\\component\\settings.py")

SPECIAL_CHAR = ("!", "@", "#", "$", "%", "^", "&", "*", "(", ")")
NUMBER = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
UPPER_CASE = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
              "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y",
              "Z")

LOWER_CASE = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
              "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")
