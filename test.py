import gatoryaml

# header = {"break": True, "fastfail": True, "List": ["One", "Two"]}
body = {
   'gatorconfig/main/java/samplelab/SampleLabMain.java': ['--one 1 --two 2 --three 3', '--uno 1 --dos 2'],
   'gatorconfig/main/java/samplelab/DataClass.java': ['--one 1 --two 2 --three 3', '--ichi 1 --ni 2'],
   'writing/reflection.md': ['--one 1 --two 2 --three 3']
}

# body = {"listy!": ["item1", "Item2", True]}

print(gatoryaml.split_file_path(body))
