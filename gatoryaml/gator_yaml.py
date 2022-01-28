"""Converts dictionaries to GatorYAML"""
from gatorconfig.split_file_path import split_file_path


class GatorYaml:
    """Main GatorYaml object"""

    def __init__(self, indent=4, spaces=4):
        """Init GatorYAML object. Takes optional arguments to change indent of files
        and how many spaces is considered a tab """
        self.spaces = spaces  # How many spaces is a tab
        self.tabs = -1  # Current tab level
        self.output = ""  # Init output
        self.keywords = ["(pure)", "commits"]  # Any keywords to look for
        self.indents = indent  # set indent for file path

    def dump(self, dic, paths=None):
        """Input dictionary is parsed. returns string of valid YAML"""

        if paths is not None:
            if isinstance(paths, dict):
                dic["files"] = split_file_path(paths)
            else:
                raise Exception("Paths expected to be \"dict\", got " + str(type(paths)) + "!")

        self.enum_dict(dic)

        return self.output

    def enum_list(self, list_in):
        """Enumerate through input list and output each item unless it finds another dictionary."""
        for i in list_in:
            if isinstance(i, dict):
                self.tabs += 1
                self.enum_dict(i)
            else:
                self.output_list_item(i)

    def enum_dict(self, dic):
        """Enumerate through input dictionary and output each key"""
        self.tabs += 1

        for k in dic.keys():
            if k == "indent":
                self.indents = int(dic[k])

            if k == "files":
                self.tabs -= 1
                # if isinstance(d[k], list):
                #     self.enum_list(d[k])
                if isinstance(dic[k], dict):
                    self.enum_file_dict(dic[k])
            elif isinstance(dic[k], list):
                self.output_key(k)
                self.enum_list(dic[k])
            elif isinstance(dic[k], dict):
                self.output_key(k)
                self.enum_dict(dic[k])
            else:
                if not self.is_keyword(k, dic[k]):
                    self.output_key_value(k, dic[k])

        self.tabs -= 1

    def enum_file_dict(self, files):
        """Enumerate through the file list dictionary and output each key"""
        self.tabs += 1

        for k in files:
            if isinstance(files[k], dict):
                self.output_key(k)
                self.enum_file_dict(files[k])
            elif isinstance(files[k], list):
                self.output_key(k)
                self.enum_file_list(files[k])

        self.tabs -= 1

    def enum_file_list(self, list_in):
        """Enumerate through each file key's parameter list items"""
        for item in list_in:
            self.output += (" " * self.spaces) * self.indents + str(item) + "\n"

    def output_list_item(self, item):
        """Output a generic list item"""
        self.output += (" " * self.spaces) * self.tabs + " -" + str(item) + "\n"

    def output_key(self, key):
        """Output a generic key"""
        self.output += (" " * self.spaces) * self.tabs + str(key) + ":\n"

    def output_key_value(self, key, value):
        """Output a generic key and it's value"""
        self.output += ((" " * self.spaces) * self.tabs) + str(key) + ": " + str(value) + "\n"

    def is_keyword(self, key, value):
        """Output key and value if a keyword"""
        if key in self.keywords:
            if key == "commits":
                self.output += (" " * self.spaces) * self.tabs \
                               + "--" + str(key) + " " + str(value) + "\n"
            else:
                self.output += (" " * self.spaces) * self.tabs + str(key) \
                               + " " + str(value) + "\n"
            return True
        return False
