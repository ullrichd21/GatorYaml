import gatoryaml

header = {
    "name": "gatorgrader-samplelab",
    "break": True,
    "fastfail": False,
    "indent": 4,
    "idcommand": "echo $TRAVIS_REPO_SLUG",
    "version": "v0.2.0",
    "executables": ["cat", "bash"],
    "startup": "./config/startup.sh",
    "reflection": "writing/reflection.md"
}

body = {
    "src/main/java/samplelab/SampleLabMain.java": ["--exists", "--single 1 --language Java",
                                                   "--multi 3 --language Java",
                                                   "--fragment \"println(\" --count 2",
                                                   "--fragment \"new DataClass(\" --count 1",
                                                   "--regex \"new\s+\S+?\(.*?\)\" --count 2 --exact"],
    "src/main/java/samplelab/DataClass.java": ["--exists", "--multi 1 --language Java", "--single 1 --language Java",
                                               "--fragment \"int \" --count 1"],
    "writing": "(pure) test",
    "writing/reflection.md": ["mdl", "cat", "--paragraphs 2", "--words 6"],
    "--commits 18": ""
}
# body = {'gatorconfig/main/java/samplelab/SampleLabMain.java': [''],
#     'gatorconfig/main/java/samplelab/DataClass.java': ['']}

print(gatoryaml.dump(header, body))
