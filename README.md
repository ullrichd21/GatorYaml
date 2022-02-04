# GatorYAML

![GatorYAML Logo](https://i.imgur.com/E4masCO.png)

Custom YAML-like generator for GatorGrader config files.

## General installation:

You can install GatorYAML from PyPi using pip:
`pip install gatoryaml`

## Basic Usage:

Basic usage is very simple. Just import GatorYAML and provide the `dump` function with a header and body. That function returns a formatted string you can drop right into a file!
```python
import gatoryaml

header = {"option":"value"}
body = {"some/file/path.md":["--options!", "new lines are list indexes", "all file parameters must be a list"],
        "some/other/folder":"Otherwise it's output as (pure) text!"}

print(gatoryaml.dump(header, body))
```

## Contributing:

To contribute, please make sure your code passes all test cases and linting before creating a pull request!
