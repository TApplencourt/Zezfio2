from ctypes import c_int,c_long,c_float,c_double,c_char
from collections import namedtuple

def strbool2int(b):
  "1 is True, 0 is False"
  if b in 'Tt1':
     return 1
  elif b in 'Ff0':
     return 0
  else:
     raise TypeError("strbool2int : %s should be in (T|F)"%b)

#c_type is for allocate the array for the c binding
Convert = namedtuple("Convert", ["str_size", "c_size", "c_type","py_array_code", "fortran_type", "str2py"])
c2stuff = {
    "bool"   :   Convert(24,  4,  c_int,    'i', "LOGICAL",          strbool2int ),
    "int"    :   Convert(24,  4,  c_int,    'i', "INTEGER",          int         ),
    "long"   :   Convert(24,  8,  c_long,   'l', "INTEGER*8",        int         ),
    "float"  :   Convert(24,  4,  c_float,  'f', "REAL",             float       ),
    "double" :   Convert(32,  8,  c_double, 'd', "DOUBLE PRECISION", float       )
}

def ljust2(str_):
  return str_.ljust(int(str_type[5:-1]))

for i in range(3000):
  c2stuff["char[%d]"%i] = Convert(i+1,i,c_char,'c', "CHARACTER*(%d)"%i, ljust2)

def is_char(str_type):
  if "char[" in str_type:
    return True
  else:
    return False

import array
def bytes2array(ctypes,bytes):
  
  padding = is_char(ctypes)
  try:
    code = c2stuff[ctypes].py_array_code
  except KeyError:
    raise KeyError("Cannot convert %s into array"%ctypes) 

  c_array = array.array(code,bytes)
  return c_array

def array2size(ctypes,carray):
  return c_int(len(carray)*c2stuff[ctypes].c_size)

def len2bytes(ctypes,len_=1):
  return c_int(c2stuff[ctypes].c_size*len_)


def type_fortran2c(ftype):
    for ctype, t in c2stuff.iteritems():
        if ftype.lower() == t.fortran_type.lower():
            return ctype
    raise AttributeError, "Not C type for Fortran type: %s" % ftype

