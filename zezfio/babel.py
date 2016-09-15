from ctypes import c_int,c_long,c_float,c_double,create_string_buffer
from collections import namedtuple

def strbool2int(b):
  "1 is True, 0 is False"
  if b in 'Tt1':
     return 1
  elif b in 'Ff0':
     return 0
  else:
     raise TypeError("strbool2int : %s should be in (T|F)"%b)

def ljust2(str_,t_interface):
  padding = int(t_interface[5:-1])
  return str_.ljust(padding)

#c_type is for allocate the array for the c binding
Convert = namedtuple("Convert", ["str_size", "c_size", "c_type","py_array_code", "fortran_type", "str2py"])
c2stuff = {
    "bool"   :   Convert(24,  4,  c_int,    'i', "LOGICAL",          strbool2int ),
    "int"    :   Convert(24,  4,  c_int,    'i', "INTEGER",          int         ),
    "long"   :   Convert(24,  8,  c_long,   'l', "INTEGER*8",        int         ),
    "float"  :   Convert(24,  4,  c_float,  'f', "REAL",             float       ),
    "double" :   Convert(32,  8,  c_double, 'd', "DOUBLE PRECISION", float       )
}

for i in range(3000):
  c2stuff["char[%d]"%i] = Convert(i+1,i,create_string_buffer,'c', "CHARACTER*(%d)"%i, ljust2)

def is_char(t_interface):
  if "char[" in t_interface:
    return True
  else:
    return False

from operator import mul
def shape2nele(l):
  return reduce(mul, l)

#We need the len because, if the data_interface is a c_pointer it's iterable!
def buffer_interface2py(data_interface,nele=0):

  if nele:
    return [data_interface[i] for i in range(nele)]
  else:
    return data_interface[0]

def nele2bytes_interface(t_interface,nele=1):
  return c_int(c2stuff[t_interface].c_size*nele)


import array
def bytes2interface(t_interface,bytes):

  if is_char(t_interface):
    data_interface = bytes
  else:
    try:
      code = c2stuff[t_interface].py_array_code
    except KeyError:
      raise KeyError("Cannot convert %s into array"%t_interface) 
    else:  
      data_interface = array.array(code,bytes)
    
  return data_interface


def py2interface(t_interface,data_py):

  if is_char(t_interface):
    data_interface = data_py
  else:
    try:
      code = c2stuff[t_interface].py_array_code
    except KeyError:
      raise KeyError("Cannot convert %s into array"%t_interface) 
    
    if type(data_py) is list:  
      data_py_array = data_py
    else:
      data_py_array = [data_py]

    data_interface = array.array(code,data_py_array)
    
  return data_interface

def type_fortran2c(t_fortran):
    for ctype, t in c2stuff.iteritems():
        if t_fortran.lower() == t.fortran_type.lower():
            return ctype
    raise AttributeError, "Not C type for Fortran type: %s" % t_fortran

