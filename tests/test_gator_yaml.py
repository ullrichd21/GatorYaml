"""Testing for gator_yaml"""
import pytest
import gatoryaml


@pytest.mark.parametrize(
    "key,value,tabs,spaces,expected",
    [
        ("test", "", 0, 4, "test:\n"),
        ("key_1", True, 1, 2, "  key_1: True\n"),
    ],
)
def test_output_key_header(key, value, tabs, spaces, expected):
    """Test for gator_yaml output_key function"""
    assert gatoryaml.output_key_header(key, value=value, tabs=tabs, spaces=spaces) == expected


@pytest.mark.parametrize(
    "header,expected",
    [
        ({"break": True, "fastfail": True, "List": ["One", "Two"]},
         "break: True\nfastfail: True\nList: One, Two\n"),
        ({"break": True}, "break: True\n"),
        ({"listy!": ["item1", "Item2", True]}, "listy!: item1, Item2, True\n"),
    ],
)
def test_parse_header(header, expected):
    """Test for gator_yaml dump function"""
    assert gatoryaml.parse_header(header) == expected


@pytest.mark.parametrize(
    "body,expected",
    [
        ({'gatorconfig': {'main':
                              {'java': {'samplelab':
                                            {'SampleLabMain.java': ['--one 1 --two 2 --three 3', '--uno 1 --dos 2'],
                                             'DataClass.java': ['--one 1 --two 2 --three 3', '--ichi 1 --ni 2']}}}},
          'writing': {'reflection.md': ['--one 1 --two 2 --three 3']}}, "gatorconfig:\n    main:\n        "
                                                                        "java:\n            samplelab:\n"
                                                                        "                SampleLabMain.java:\n"
                                                                        "                --one 1 --two 2 --three 3\n"
                                                                        "                --uno 1 --dos 2\n"
                                                                        "                DataClass.java:\n"
                                                                        "                --one 1 --two 2 --three 3\n"
                                                                        "                --ichi 1 --ni 2\nwriting:\n"
                                                                        "    reflection.md:\n"
                                                                        "                --one 1 --two 2 --three 3\n"),
        ({"listy!": ["item1", "Item2", True]}, "listy!:\n                item1\n"
                                               "                Item2\n                True\n"),
        ({"commits": ""}, "commits\n"),
        ({"commits": None}, "commits\n")
    ],
)
def test_parse_body(body, expected):
    """Test for gator_yaml dump function"""
    assert gatoryaml.parse_body(body) == expected


@pytest.mark.parametrize(
    "list_in,spaces,indent,expected",
    [
        (["--test 1", "--test 2"], 4, 2, "        --test 1\n        --test 2\n"),
        (["--single 1 --language Java"], 4, 0, "--single 1 --language Java\n"),
    ],
)
def test_print_list_body(list_in, spaces, indent, expected):
    """Test for gator_yaml enum_file_list function"""
    assert gatoryaml.print_list_body(list_in, spaces=spaces, indent=indent) == expected
