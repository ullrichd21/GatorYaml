"""Converts dictionaries to GatorYAML"""


def dump(header, body, indent=4, spaces=4):
    """Input dictionary is parsed. returns string of valid YAML"""
    return Parser(header, body, indent, spaces).do_parse()


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

    def enum_dict_body(self, body):
        """Enumerate through the file list dictionary and output each key"""
        self.tabs += 1

        for key in body:
            if isinstance(body[key], dict):
                self.output_key_header(key)
                self.enum_dict_body(body[key])
            elif isinstance(body[key], list):
                self.output_key_header(key)
                self.enum_list_body(body[key])

        self.tabs -= 1

    def enum_list_body(self, list_in):
        """Enumerate through each file key's parameter list items"""
        for item in list_in:
            self.output += (" " * self.spaces) * self.indents + str(item) + "\n"

    def output_list_item_header(self, item):
        """Output a generic list item"""
        self.output += (" " * self.spaces) * self.tabs + " -" + str(item) + "\n"

    def output_key_header(self, key, value="", pure=False):
        """Output a key"""
        if pure:
            self.output += (" " * self.spaces) * self.tabs + str(key) + "\n"
        if value != "":  # Append a space to value if it exists.
            value = " " + str(value) + " "
        self.output += (" " * self.spaces) * self.tabs + str(key) + ":" + value + "\n"


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
