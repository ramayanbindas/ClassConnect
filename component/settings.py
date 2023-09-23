'''
# version: 1.0.0
:about: This module contains all the necessary constants, settings need for the
application,

'''

from os.path import abspath

# if the application runs over the window.
BASEFILEPATH = abspath(__file__).removesuffix("\\component\\settings.py")

# Application Colors #
ERROR_COLOR = (1, 0, 0, 1)
