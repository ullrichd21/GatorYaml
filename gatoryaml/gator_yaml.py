"""Converts dictionaries to GatorYAML"""
from .exceptions import UnexpectedValue


def dump(header, body, indent=4, spaces=4) -> str:
    """Input dictionary is parsed. returns string of valid YAML"""

    output = parse_header(header)
    output += "---\n"
    output += parse_body(split_file_path(body), indent=indent, spaces=spaces)
    return output


def parse_header(header) -> str:
    """Parses header dictionary"""
    out = ""
    for key, val in header.items():
        out += str(key) + ": "

        if isinstance(val, list):
            out += ", ".join(str(x) for x in val)
            out += "\n"
        else:
            out += str(val) + "\n"
    return out


# pylint: disable=R0913
# Disabled because the extra parameters are for internal use.
def parse_body(body, output="", tabs=-1, indent=4, spaces=4, custom_keywords=None) -> str:
    """Enumerate through the body dictionary and output each key & values.
    If a keyword is found, special output instructions can be defined.
    If the dictionary key has no value it will be output as a parameter."""
    keywords = ["(pure)"]
    if custom_keywords is not None:
        if isinstance(custom_keywords, list):
            keywords += custom_keywords
        else:
            raise Exception("Expected a list for custom_keywords, got " + str(type(custom_keywords)))

    tabs += 1
    for key in body:
        if isinstance(body[key], dict):
            output += output_key_header(key, tabs=tabs, spaces=spaces)
            output = parse_body(body[key], tabs=tabs, output=output)
        elif isinstance(body[key], list):
            output += output_key_header(key, tabs=tabs, spaces=spaces)
            output = print_list_body(body[key], output=output, spaces=spaces, indent=indent)
        elif key in keywords:
            output += str(key) + "\n"
        elif body[key] is None or body[key] == "":
            output += str(key) + "\n"
        else:
            raise UnexpectedValue(f"{str(body[key])} was not an expected value.")

    tabs -= 1
    return output


def print_list_body(list_in, output="", spaces=4, indent=4):
    """Enumerate through each file key's parameter list items"""
    for item in list_in:
        output += (" " * spaces) * indent + str(item) + "\n"

    return output


def output_key_header(key, tabs, spaces=4, value="") -> str:
    """Output a key"""
    output = ""

    if value != "":  # Prepend a space to value if it exists.
        value = " " + str(value)
    output += (" " * spaces) * tabs + str(key) + ":" + value + "\n"
    return output


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
