'''
# version: 1.0.0
:about: This module is like utils type of module contains some supporting,
type of function and classes.
'''
import json

def dump(filename: str, mode: str = "w", value: json="") -> None:
    ''':about: function used to create a specific file in the given
        path.
        :mode: dump function only write, append the data to file.
        :value: must be any thing in a json formate.
        Note: function is not for the used of read purpose.
    '''
    try:
        with open(filename, mode) as f:
            json.dump(value, f, indent=4)
    except:
        print("File not be modified or created")

def load(filename: str, mode: str= "r") -> str:
    """:about: function used for reading the file and returs the containt,
        of the file.
    """
    content = {}
    try:
        with open(filename, mode) as f:
            content = json.load(f)

        return content
    except FileNotFoundError:
        print("File doesn't exist")