"""Test split_file_path function."""

import pytest
from gatorconfig.split_file_path import split_file_path


def test_output_as_dic():
    """Ensure output is a dictionary."""
    input_dic = {"sample/file.py": ['']}
    output = split_file_path(input_dic)
    assert isinstance(output, dict)

@pytest.mark.parametrize(
    "test_input,expected",
    [({'gatorconfig/main/java/samplelab/SampleLabMain.java': [''],
    'gatorconfig/main/java/samplelab/DataClass.java': ['']},
    {'gatorconfig': {'main': {'java': {'samplelab':
    {'SampleLabMain.java': [''], 'DataClass.java': ['']}}}}}),
    ({'gatorconfig/main/java/samplelab/SampleLabMain.java': [''],
    'writing/reflection.md': ['']}, {'gatorconfig': {'main': {'java': {'samplelab':
    {'SampleLabMain.java': ['']}}}}, 'writing': {'reflection.md': ['']}}),
    ({'gatorconfig/main/java/samplelab/DataClass.java': [''],
    'gatorconfig/main/java/HelloWorld.java': ['']},
    {'gatorconfig': {'main': {'java': {'samplelab': {'DataClass.java': ['']},
    'HelloWorld.java': ['']}}}})
    ]
)

def test_dic_nesting(test_input, expected):
    """Ensure directories are nested correctly."""
    output = split_file_path(test_input)
    assert output == expected
