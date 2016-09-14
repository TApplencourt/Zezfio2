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
    "bool"   :   Convert( 1,     4,  c_int,    'i', "LOGICAL",          strbool2int                   ),
    "int"    :   Convert( 8,     4,  c_int,    'i', "INTEGER",          int                           ),
    "long"   :   Convert( 8,     8,  c_long,   'l', "INTEGER*8",        int                           ),
    "float"  :   Convert(16,     4,  c_float,  'f', "REAL",             float                         ),
    "double" :   Convert(32,     8,  c_double, 'd', "DOUBLE PRECISION", float                         ),
    "char[512]": Convert(513,  512,  c_char,   'c', "CHARACTER*(512)",  lambda s: "%s"%(s.ljust(512)) ),
    "char[256]": Convert(257,  256,  c_char,   'c', "CHARACTER*(256)",  lambda s: "%s"%(s.ljust(256)) ),
    "char[128]": Convert(129,  128,  c_char,   'c', "CHARACTER*(128)",  lambda s: "%s"%(s.ljust(128)) ),
    "char[64]" : Convert( 65,   64,  c_char,   'c', "CHARACTER*(64)",   lambda s: "%s"%(s.ljust(64))  ),
    "char[32]" : Convert( 33,   32,  c_char,   'c', "CHARACTER*(32)",   lambda s: "%s"%(s.ljust(32))  ),
    "char[16]" : Convert( 17,   16,  c_char,   'c', "CHARACTER*(16)",   lambda s: "%s"%(s.ljust(16))  ),
    "char[8]"  : Convert(  9,    8,  c_char,   'c', "CHARACTER*(8)",    lambda s: "%s"%(s.ljust(8))   ),
    "char[4]"  : Convert(  5,    4,  c_char,   'c', "CHARACTER*(4)",    lambda s: "%s"%(s.ljust(4))   ),
    "char[2]"  : Convert(  3,    2,  c_char,   'c', "CHARACTER*(2)",    lambda s: "%s"%(s.ljust(2))   ),
}

import array
def bytes2array(ctypes,bytes):
  try:
    code = c2stuff[ctypes].py_array_code
  except KeyError:
    raise KeyError("Cannot convert %s into array"%ctypes) 

  c_array = array.array(code,bytes)
  return c_array

def array2size(ctypes,carray):
  return c_int(len(carray)*c2stuff[ctypes].c_size)
