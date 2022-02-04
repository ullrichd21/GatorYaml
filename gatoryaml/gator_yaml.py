"""Converts dictionaries to GatorYAML"""
from typing import Tuple
from .exceptions import UnexpectedValue


def dump(header, body, indent=4) -> str:
    """Input dictionary is parsed. returns string of valid YAML"""
    output = "---\n"
    header_out, indent = parse_header(header, indent)
    output += header_out
    output += "---\n"
    output += parse_body(split_file_path(body), indent=indent)
    return output


def parse_header(header, indent=4) -> Tuple[str, int]:
    """Parses header dictionary"""
    out = ""
    for key, val in header.items():
        out += str(key) + ": "

        if isinstance(val, list):
            out += ", ".join(str(x) for x in val)
            out += "\n"
        else:
            out += str(val) + "\n"

        if key == "indent":
            indent = val

    return out, indent


def parse_body(body, output="", tabs=-1, indent=4, custom_keywords=None) -> str:
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
            output += output_key_header(key, tabs=tabs, indent=indent)
            output = parse_body(body[key], tabs=tabs, output=output)
        elif isinstance(body[key], list):
            output += output_key_header(key, tabs=tabs, indent=indent)
            output = print_list_body(body[key], tabs=tabs, output=output, indent=indent)
        elif any(keyword in str(body[key]) for keyword in keywords):
            output += (" " * indent) * tabs + str(body[key]) + "\n"
        elif body[key] is None or body[key] == "":
            output += (" " * indent) * tabs + str(key) + "\n"
        else:
            raise UnexpectedValue(f"{str(key)} with value {body[key]} was not an expected value.")

    tabs -= 1
    return output


def print_list_body(list_in, tabs, output="", indent=4):
    """Enumerate through each file key's parameter list items"""
    tabs += 1
    for item in list_in:
        output += (" " * indent) * tabs + str(item) + "\n"
    return output


def output_key_header(key, tabs, value="", indent=4) -> str:
    """Output a key"""
    output = ""

    if value != "":  # Prepend a space to value if it exists.
        value = " " + str(value)
    output += (" " * indent) * tabs + str(key) + ":" + value + "\n"
    return output


def split_file_path(paths: dict) -> dict:
    """Convert files paths stored in a dict to nested dicts.
    Author: @PaigeCD / Paige Downey"""
    output = {}
    popped = {}
    for key, value in paths.items():
        if value is not None and value != "":
            directories = key.split('/')
            dir_dic = output

            for directory in directories[:-1]:
                if directory not in dir_dic:
                    dir_dic[directory] = {}
                dir_dic = dir_dic[directory]
            try:
                dir_dic[directories[-1]] = value
            except TypeError:
                print(f"Something went wrong trying to add {directories[-1]} to the following dictionary:\n{dir_dic}\n")
        else:
            popped[key] = value

    return {**output, **popped}
