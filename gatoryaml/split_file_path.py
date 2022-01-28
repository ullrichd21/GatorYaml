"""Split file path module."""


def split_file_path(paths: list) -> dict:
    """Convert files paths stored in a dict to nested dicts."""
    output = {}
    for key, value in paths.items():
        directories = key.split('/')
        dir_dic = output
        for direc in directories[:-1]:
            if direc not in dir_dic:
                dir_dic[direc] = {}
            dir_dic = dir_dic[direc]
        dir_dic[directories[-1]] = value

    return output

# example dictionary containing three file paths
# path_dic = {
#    'gatorconfig/main/java/samplelab/SampleLabMain.java': [''],
#    'gatorconfig/main/java/samplelab/DataClass.java': [''],
#    'writing/reflection.md': ['']
# }
# final_dic = split_file_path(path_dic)
# print(final_dic)
