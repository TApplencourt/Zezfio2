```bash
$ pip install jinja2 irpy
$ cd zezfio/io
$ make
$ cd ..
$ ./legacy2json.py ../install/EZFIO/config/* > x.json
$ ./fang.py x.json > fortran/ezfio.f90
$ cd fortran
$ cp $QP_ROOT/install/_build/f77_zmq-master/f77_zmq.h .
$ gfortran -O2 -g -ffree-line-length-none -fPIC -c *.f90
$ ar crv libezfio.a ezfio.o zezfio.o 
$ 

```

