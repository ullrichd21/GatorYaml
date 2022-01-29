import gatoryaml

header = {"break": True, "fastfail": True, "List": ["One", "Two"], "Multilevel": {"Test1": "one"}}
body = {
   'gatorconfig/main/java/samplelab/SampleLabMain.java': [''],
   'gatorconfig/main/java/samplelab/DataClass.java': [''],
   'writing/reflection.md': ['']
}

print(gatoryaml.dump(header, body))