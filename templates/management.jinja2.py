import irpy

from zezfio.io import zarray
from zezfio.io import zscalar
from zezfio.io.__init__ import build_path

d_instance = dict()
from ctypes import c_int
d_instance["zezfio_id"] = c_int(0)


from operator import mul
from zezfio.babel import array2size, bytes2array


def update_zezfio_id():
    d_instance["zezfio_id"] = c_int(d_instance["zezfio_id"].value + 1)

{% for category, attributes in json_config.iteritems() %}

class {{ category|capitalize }}(object):

    {% for variable in attributes["attributes"] %}

    @irpy.lazy_property
    def {{ variable.name }}_cbytes(self):
        #array2size -> dimension2size
        return array2size('{{ variable.type }}', self.{{ variable.name }}_c)

        {% if variable.dimension == '1' %}

    @irpy.lazy_property
    def {{ variable.name }}_path(self):
        return build_path('{{db_path}}','{{ category }}','{{ variable.name }}')

    @irpy.lazy_property_mutable
    def {{ variable.name }}_c(self):
        return zscalar.read_scalar(self.{{variable.name}}_path,'{{ variable.type }}')

    @irpy.lazy_property
    def {{ variable.name }}(self):
        return self.{{variable.name}}_c[0]

    def set_{{ variable.name }}(self,bytes):

        c_array = bytes2array('{{ variable.type }}', bytes)

        self.{{ variable.name }}_c = c_array
        zscalar.write_scalar(self.{{ variable.name }}_path,self.{{ variable.name }})

        update_zezfio_id()

        {% else %}
    @irpy.lazy_property_mutable
    def {{ variable.name }}_shape(self):
        return {{variable.dimension}}

    @irpy.lazy_property
    def {{ variable.name }}_slen(self):
        return reduce(mul, self.{{ variable.name }}_shape)

    @irpy.lazy_property
    def {{ variable.name }}_path(self):
        return build_path('{{db_path}}','{{ category }}','{{ variable.name }}',array=True)

    @irpy.lazy_property_mutable
    def {{ variable.name }}_c(self):
        return zarray.read_array(self.{{variable.name}}_path,'{{ variable.type }}',self.{{ variable.name }}_slen)

    @irpy.lazy_property
    def {{ variable.name }}(self):
        c_data = self.{{ variable.name}}_c
        return [c_data[i] for i in range(self.{{ variable.name }}_slen)]

    def set_{{ variable.name }}(self,bytes):

        c_array = bytes2array('{{ variable.type }}', bytes)

        slen = self.{{ variable.name }}_slen
        sgiven = len(c_array) 
        if  slen != sgiven:
            raise IndexError("Conflic between the spec len of the array %i and the given one %i" % (slen, sgiven))       


        self.{{ variable.name }}_c = c_array
        zarray.write_array(self.{{ variable.name }}_path,
                           self.{{ variable.name }}_shape, 
                           self.{{ variable.name }})


        update_zezfio_id()

        {% endif %}
    {% endfor %}

#For allowing referance in shape
{{ category }} = {{ category|capitalize }}()
#Quicker than getattr
d_instance[ "{{ category }}" ] = {{ category }}

{%  endfor %}
