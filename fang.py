#!/usr/bin/env python
if __name__ == '__main__':

    #  _             
    # |_) _. _|_ |_  
    # |  (_|  |_ | | 
    #
    import sys
    path_config = sys.argv[1]

    #                                     _       
    # |_|  _. ._   _| |  _     _  _  ._ _|_ o  _  
    # | | (_| | | (_| | (/_   (_ (_) | | |  | (_| 
    #                                          _|
    from zezfio.template import template_generator
    template = template_generator.generate_fortran(path_config)

    print template