```bash
$ pip install jinja2 irpy
$ cd zezfio/io
$ make
$ ./legacy2json.py ../install/EZFIO/config/* > x.json
$ fang x.json > fortran/ezfio.f90
$ cp $QP_ROOT/install/_build/f77_zmq-master/f77_zmq.h .
$ gfortran -ffree-line-length-none -fPIC -c *.f90
$ ar crv libezfio.a ezfio.o zezfio.o 
$ 

```

