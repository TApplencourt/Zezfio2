import os

def build_path(root_path,category,raw_name,array=False):
    if array:
        name = "%s.gz"%raw_name
    else:
        name = raw_name

    path = os.path.join(root_path, category, name)
    if not os.path.isfile(path):
        raise IOError("%s doesn't exist" % path)

    return path