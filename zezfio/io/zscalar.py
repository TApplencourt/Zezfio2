from zezfio import babel
import array

def db2py(path,t_interface):
    "Return array c_type"

    with open(path, 'r') as f:
        data = f.read().strip()

    #Raw -> Python
    try:
        f = babel.c2stuff[t_interface].str2py
    except KeyError:
        raise TypeError, "Error: cannot convert str to %s" % t_interface
    
    #We need to do the padding
    if not babel.is_char(t_interface):
        py_data = f(data)
    else:
        py_data = f(data,t_interface)

    return py_data

#Need to be and array or a string
def interface2db(path, py_scalar):

    if type(py_scalar) == str:
        data = py_scalar
    else:
        data = str(py_scalar[0])

    with open(path, 'w') as f:
        f.write("%s\n" % data)

