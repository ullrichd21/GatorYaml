"""Testing for gator_yaml"""
import pytest
from gatorconfig.gator_yaml import GatorYaml


@pytest.mark.parametrize(
    "key,expected",
    [
        ("test", "test:\n"),
        ("key_1", "key_1:\n"),
        ("key2", "key2:\n"),
    ],
)
def test_output_key(key, expected):
    """Test for gator_yaml output_key function"""
    yaml = GatorYaml()
    yaml.output_key(key)
    assert yaml.output == expected


@pytest.mark.parametrize(
    "key, value, expected",
    [
        ("test", "value", "test: value\n"),
        ("key_1", "value 1", "key_1: value 1\n"),
        ("key2", "value that is longer!", "key2: value that is longer!\n"),
    ],
)
def test_output_key_value(key, value, expected):
    """Test for gator_yaml output_key_value function"""
    yaml = GatorYaml()
    yaml.output_key_value(key, value)
    assert yaml.output == expected


@pytest.mark.parametrize(
    "key,value,expected",
    [
        ("key", "value", False),
        ("(pure)", "good value", True),
        ("(pure)", "(pure) Code", True),
    ],
)
def test_is_keyword(key, value, expected):
    """Test for gator_yaml is_keyword function"""
    yaml = GatorYaml()
    assert yaml.is_keyword(key, value) == expected


@pytest.mark.parametrize(
    "item,expected",
    [
        ("item1", " -item1\n"),
        ("item 2", " -item 2\n"),
        ("item_3", " -item_3\n"),
    ],
)
def test_output_list_item(item, expected):
    """Test for gator_yaml output_list_item function"""
    yaml = GatorYaml()
    yaml.output_list_item(item)
    assert yaml.output == expected


@pytest.mark.parametrize(
    "dic,expected",
    [
        ({"test": "Bing bong", "test2": ["bing", "bong"], "test3":
            {"Indent!": "wooooo!", "wanna see me do it again?": {
                "Bada-bing": "bada-boom!", "list?": ["Hello", "Steve"]}}, "test4": "Continue?"},
         "test: Bing "
         "bong\ntest2:\n -bing\n -bong\ntest3:\n    Indent"
         "!: wooooo!\n    wanna see me do it again?:\n"
         "        Bada-bing: bada-boom!\n        list"
         "?:\n         -Hello\n"
         "         -Steve\ntest4: "
         "Continue?\n"),
        ({"break": True}, "break: True\n"),
        ({"listy!": ["item1", "Item2", True]}, "listy!:\n -item1\n -Item2\n -True\n"),
        ({"(pure)": "pure output!"}, "(pure) pure output!\n"),
        ({"commits":10}, "--commits 10\n")
    ],
)
def test_dump(dic, expected):
    """Test for gator_yaml dump function"""
    yaml = GatorYaml()
    # print(yaml.dump(dic))
    assert yaml.dump(dic) == expected


@pytest.mark.parametrize(
    "list_in,expected",
    [
        (["--test 1", "--test 2"], "                --test 1\n                --test 2\n"),
        (["--single 1 --language Java"], "                --single 1 --language Java\n"),
    ],
)
def test_enum_file_list(list_in, expected):
    """Test for gator_yaml enum_file_list function"""
    yaml = GatorYaml()
    yaml.enum_file_list(list_in)
    assert yaml.output == expected


@pytest.mark.parametrize(
    "files,expected",
    [
        ({'gatorconfig': {'main': {'java': {'test.java': ['']}}}},
         "gatorconfig:\n    main:\n        java:\n        "
         "    test.java:\n                \n"),
        ({'gatorconfig': {'main': {'java': {'test.java': [''], 'test2.java': ['']}}}},
         "gatorconfig:\n    main:\n        java:\n            "
         "test.java:\n                \n            test2.java:\n       "
         "         \n"),
    ],
)
def test_enum_file_dict(files, expected):
    """Test for gator_yaml enum_file_dict function"""
    yaml = GatorYaml()
    yaml.enum_file_dict(files)
    assert yaml.output == expected
