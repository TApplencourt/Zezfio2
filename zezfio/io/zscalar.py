from zezfio import babel
import array
import os

def read_scalar(path,type_):
    "Return array c_type"

    with open(path, 'r') as f:
        data = f.read().strip()

    #Str -> Python
    try:
        f = babel.c2stuff[type_].str2py
    except KeyError:
        raise TypeError, "Error: cannot convert str to %s" % type_
    else:
        try:
            py_data = f(data)
        except TypeError:   # for strings
            py_data = data.ljust(f)

    #Python -> C_type
    try:
        code = babel.c2stuff[type_].py_array_code
    except KeyError:
        raise TypeError, "Error: cannot convert %s to %s" % (py_data, type_)

    if code == 'c':
      result = array.array(code,py_data)
    else:
      result = array.array(code,[py_data])
    return result

def write_scalar(path, py_scalar):

    with open(path, 'w') as f:
        f.write("%s\n" % str(py_scalar))

