# pylint: skip-file
"""Converts dictionaries to GatorYAML"""
from gatoryaml.exceptions import *


def dump(header, body, indent=4, spaces=4) -> str:
    """Input dictionary is parsed. returns string of valid YAML"""

    output = parse_header(header)
    b = split_file_path(body)
    print(f"-----\n{b}\n")
    output += parse_body(b, indent=indent, spaces=spaces)
    return output

    # return Parser(header, body, indent, spaces).do_parse()


def parse_header(header) -> str:
    out = ""
    for key, val in header.items():
        out += str(key) + ": "

        if isinstance(val, list):
            for element in val:
                if element != val[-1]:
                    out += element + ", "
                else:
                    out += element + "\n"
        else:
            out += str(val) + "\n"
    return out


def parse_body(body, output="", tabs=-1, indent=4, spaces=4, keywords=[]) -> str:
    """Enumerate through the body dictionary and output each key & values.
    If a keyword is found, special output instructions can be defined.
    If the dictionary key has no value it will be output as a parameter."""

    keywords = ["(pure)"] + keywords

    tabs += 1
    for key in body:
        if isinstance(body[key], dict):
            output += output_key_header(key, tabs=tabs, spaces=spaces)
            output = parse_body(body[key], tabs=tabs, output=output)
        elif isinstance(body[key], list):
            output += output_key_header(key, tabs=tabs, spaces=spaces)
            output = enum_list_body(body[key], output=output, spaces=spaces, indent=indent)
        elif key in keywords:
            output += key + "\n"
        elif body[key] is None or body[key] == "":
            output += "--" + key + "\n"
        else:
            raise UnexpectedValue(f"{str(body[key])} was not an expected value.")

    tabs -= 1
    return output


def enum_list_body(list_in, output="", spaces=4, indent=4):
    """Enumerate through each file key's parameter list items"""
    for item in list_in:
        output += (" " * spaces) * indent + str(item) + "\n"

    return output


def output_key_header(key, tabs, spaces=4, value="", pure=False) -> str:
    """Output a key"""

    output = ""

    if pure:
        output += (" " * spaces) * tabs + str(key) + "\n"
    if value != "":  # Append a space to value if it exists.
        value = " " + str(value) + " "
    output += (" " * spaces) * tabs + str(key) + ":" + value + "\n"
    return output


class Parser:
    """Parser object"""

    def __init__(self, header, body, indent=4, spaces=4):
        """Init GatorYAML object. Takes optional arguments to change indent of files
        and how many spaces is considered a tab """
        self.spaces = spaces  # How many spaces is a tab
        self.tabs = -1  # Current tab level
        self.output = ""  # Init output
        self.keywords = ["(pure)"]  # Any keywords to look for
        self.indents = indent  # set indent for file path
        self.header = header
        self.body = body

    def do_parse(self):
        self.enum_dict_header(self.header)
        self.enum_dict_body(split_file_path(self.body))

        return self.output

    def enum_list_header(self, list_in):
        """Enumerate through input list and output each item unless it finds another dictionary."""
        for i in list_in:
            if isinstance(i, dict):
                self.tabs += 1
                self.enum_dict_header(i)
            else:
                self.output_list_item_header(i)

    def enum_dict_header(self, header):
        """Enumerate through input dictionary and output each key"""
        self.tabs += 1

        for key in header.keys():
            if isinstance(header[key], list):
                self.output_key_header(key)
                self.enum_list_header(header[key])
            elif isinstance(header[key], dict):
                self.output_key_header(key)
                self.enum_dict_header(header[key])
            else:
                if header[key] == "":
                    self.output_key_header(key, pure=True)
                else:
                    self.output_key_header(key, value=header[key])

        self.tabs -= 1

    def output_list_item_header(self, item):
        """Output a generic list item"""
        self.output += (" " * self.spaces) * self.tabs + " -" + str(item) + "\n"


def split_file_path(paths: dict) -> dict:
    """Convert files paths stored in a dict to nested dicts.
    Author: @PaigeCD / Paige Downey"""
    output = {}
    for key, value in paths.items():
        directories = key.split('/')
        dir_dic = output
        for directory in directories[:-1]:
            if directory not in dir_dic:
                dir_dic[directory] = {}
            dir_dic = dir_dic[directory]
        dir_dic[directories[-1]] = value

    return output
