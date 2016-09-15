from zezfio import babel
import array

def db2py(path,type_):
    "Return array c_type"

    with open(path, 'r') as f:
        data = f.read().strip()

    #Str -> Python
    try:
        f = babel.c2stuff[type_].str2py
    except KeyError:
        raise TypeError, "Error: cannot convert str to %s" % type_

    if not babel.is_char(type_):
        py_data = f(data)
    else:
        py_data = f(data,type_)

    return py_data

def write_scalar(path, py_scalar):

    with open(path, 'w') as f:
        f.write("%s\n" % str(py_scalar))

