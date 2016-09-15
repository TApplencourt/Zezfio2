![](http://i.imgur.com/XUeaDoy.gif)

The lovely client/server version of [Ezfio](http://irpf90.ups-tlse.fr/index.php?title=EZFIO)

# Dependency
- [IRPy](https://github.com/TApplencourt/IRPy)
- [Jinja2](http://jinja.pocoo.org/docs/dev/)
- [Zeromq](http://zeromq.org/)
- [Pyzmq](https://github.com/zeromq/pyzmq)
- [f77_zmq](https://github.com/zeromq/f77_zmq)

You can use [pip](https://pip.pypa.io/en/stable/installing/) all the Python Dependencies and 
- `pip install irpy jinja2 pyzmq`

# Boilerplate

1) C and Config
```bash
$ cd zezfio/io ; make; cd .. #Make the C file
$ ./legacy2json.py ../install/EZFIO/config/* > config.json #Create the config file
```
2) Fortran
```bash
$ cd fortran
$ ./fang.py x.json > fortran/ezfio.f90 #Create fortran file who contain the ezfio API
$ cp $QP_ROOT/install/_build/f77_zmq-master/f77_zmq.h . #Copy the f77_zmq.h for simplicity
$ gfortran -O2 -g -ffree-line-length-none -fPIC -c *.f90 #Compile
$ ar crv libezfio.a ezfio.o zezfio.o  #Create the library
```
3) Run
```
$./server.py  <zmq_bind_address> <path_config> <db_path> &  tail -f myapp.log
$ export ZEZFIO_ADDRESS=<zmq_connection_address> ; a.out #The fortran will use this enviroment variable
```

