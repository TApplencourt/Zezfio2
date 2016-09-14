#!/usr/bin/env python
import zmq
import logging
if __name__ == '__main__':
    #                         
    # |  _   _   _  o ._   _  
    # | (_) (_| (_| | | | (_| 
    #        _|  _|        _| 
    #        
    logging.basicConfig(filename='myapp.log', level=logging.ERROR)

    #  _             
    # |_) _. _|_ |_  
    # |  (_|  |_ | | 
    #
    import sys, os
    address, path_config, db_path_rel = sys.argv[1:]
    db_path = os.path.abspath(db_path_rel)

    #                                     _       
    # |_|  _. ._   _| |  _     _  _  ._ _|_ o  _  
    # | | (_| | | (_| | (/_   (_ (_) | | |  | (_| 
    #                                          _|
    from zezfio.template import generator
    d_instance = generator.get_dict_module_server(path_config,db_path)

    #  __                 
    # (_   _  ._    _  ._ 
    # __) (/_ | \/ (/_ |  
    #
    context = zmq.Context(io_threads=4)
    sock = context.socket(zmq.REP)
    sock.bind(address)

    # ~#~#~#~#
    # Little_optimisation
    # ~#~#~#~#
    send = sock.send
    recv = sock.recv

    # ~#~#~#~#
    # Error_code
    # ~#~#~#~#    
    from ctypes import c_int
    errno_fail = c_int(-1)
    errno_success = c_int(0)

    while True:
            #For the sake of performance, inline the main loop
            #Get the info
            try:
                m = recv()
                print m
            except zmq.error.ZMQError:
                raise
                logging.error("Error when asking for a message")
                continue

            try:
                action, str_instance, name = m.split(".")
            except:
                logging.error("Error when spliting the message %s"%m)
                continue

            try:
                instance = d_instance[str_instance]
            except Exception as e:
                logging.error("Cannot get %s category" % str_instance)
                send(errno_fail)
                continue

            #Get the instance
            if action == "has":

                try:
                    getattr(instance, name)
                except Exception as e:
                    logging.error(e)
                    send(errno_fail)
                    continue
                else:
                    send(errno_success)
                    logging.debug("Is Present")

            elif action == "size":

                try:
                    size = getattr(instance, "%s_cbytes" % name)
                except Exception as e:
                    logging.error(e)
                    send(errno_fail)
                    continue
                else:
                    send(errno_success,  zmq.SNDMORE)
                    send(size)
                    logging.debug("Size send")

            elif action == "get":
                try:
                    size = getattr(instance, "%s_cbytes" % name)
                    print "size", size
                    array = getattr(instance, "%s_c" % name)
                except Exception as e:
                    logging.error(e)
                    send(errno_fail)
                    continue
                else:
                    send(errno_success,  zmq.SNDMORE)
                    send(size, zmq.SNDMORE)               
                    send(array)

            elif action == "set":
                try:
                    bytes = recv()
                except zmq.error.ZMQError:
                    logging.error("Error when reading the byte for the set")
                    continue

                try:
                    getattr(instance, "set_%s" % name)(bytes)
                except Exception as e:
                    logging.error(e)
                    send(errno_fail)
                    continue
                else:
                    errno_success = d_instance["zezfio_id"]
                    send(errno_success)
                    logging.debug("Set Done. Errno is %s" % errno_success.value)

            else:
                logging.error("Cannot understant theaction to do %s"%action)
                continue
