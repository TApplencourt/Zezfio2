import os
dir_path = os.path.dirname(os.path.realpath(__file__))
dll_path = os.path.join(dir_path,"gz2ar.so")

from ctypes import CDLL, get_errno
#Absolute path
dll = CDLL(dll_path,use_errno=True)


from zezfio import babel
from ctypes import c_char

d_erno = {100: "gzopen failed for {file}",
          101: "Your buffer size ({length} bytes) is to small for the uncompressed data for file {file}",
          102: "They are more value to read than (>{nb_scalar} asked)",
          103: "I read less value than asked (<{nb_scalar})",
          104: "Only 1 or 0 are convertible to bool"}

def check_errno():
    errno = get_errno()
    try:
        message_template = d_erno[errno]
    except KeyError:
        return buffer
    else:
        message = message_template.format(**locals())
        raise BytesWarning("Error: %s"%message)

def gzip2buffer(file,bytes,header_bytes=200):

    total_bytes = header_bytes + bytes
    buffer_type = (c_char * total_bytes)
    buffer = buffer_type()

    dll.gzip2buffer(file,total_bytes,buffer)
    check_errno()
    return buffer

#This function is IMPUR !!! Buffer will be modify !
def buffer2stuff_impur(str_type,buffer,length):

    if not babel.is_char(str_type):

        #Get the C function
        try:
            c_function = getattr(dll,"buffer2%s_impur"%str_type)
        except AttributeError:
            raise BytesWarning("Error: No C function to convert your buffer in this format: %s"%str_type)
        #Malloc the c_array
        try:
            c_type = babel.c2stuff[str_type].c_type
        except:
            raise BytesWarning("Error: No C_type related to: %s"%str_type)
        else:
            c_array_type = ( c_type * length)
            c_array = c_array_type()
    
        #Call the function
        c_function(buffer,length,c_array)

    else:
        #Get the C function
        c_function = getattr(dll,"buffer2char")
    
        #Malloc the c_array
        try:
            c_type = babel.c2stuff[str_type].c_type
            char_size = babel.c2stuff[str_type].c_size

            real_length = length*char_size
        except:
            raise BytesWarning("Error: No C_type related to: %s"%str_type)
        else:
            c_array_type = ( c_type * real_length)
            c_array = c_array_type()
    
        #Call the function
        from ctypes import c_size_t
        c_function(buffer, length,c_size_t(char_size), c_array)

    check_errno()

    return c_array


import gzip
from operator import mul
def read_array(path,str_type,slen):
    #slen = spec length
    #dlen = d length

    with gzip.open(path,"r") as f:
        f.readline()
        dlen = reduce(mul,map(int,f.readline().split()))

    if dlen != slen:
        raise BytesWarning("Error: Asked dimension (%s) and these on header on file are different (%s)"%(slen,dlen))

    try:
        str_length = slen * babel.c2stuff[str_type].str_size
    except KeyError:
        raise TypeError("Error: No size for to %s" % str_type)
    else:
        buffer = gzip2buffer(path,str_length)

    return buffer2stuff_impur(str_type,buffer,slen)


def write_array(path,shape,py_data):

        header = [str(len(shape)), 
                  "  ".join(map(str,shape))]

        if type(py_data[0]) != str:
            lstr = map(str,py_data)        
    
        else:
            lstr = [str(i) if i!='\x00' else '\n' for i in py_data]
            lstr = ["".join(lstr)]

        with gzip.open(path, 'w') as f:
            f.write("%s\n" % "\n".join(header+lstr))

