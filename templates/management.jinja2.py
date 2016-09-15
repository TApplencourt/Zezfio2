import irpy

from zezfio.io import zarray
from zezfio.io import zscalar
from zezfio.io.__init__ import build_path

d_instance = dict()
from ctypes import c_int
d_instance["zezfio_id"] = c_int(0)



from zezfio import babel


def update_zezfio_id():
    d_instance["zezfio_id"] = c_int(d_instance["zezfio_id"].value + 1)

{% for category, attributes in json_config.iteritems() %}

class {{ category|capitalize }}(object):

    {% for variable in attributes["attributes"] %}

        {% if variable.dimension == '1' %}

    @irpy.lazy_property
    def {{ variable.name }}_path(self):
        return build_path('{{db_path}}','{{ category }}','{{ variable.name }}',array=False)

    @irpy.lazy_property
    def {{ variable.name }}(self):
            {% if variable.default is not defined %}
        return zscalar.db2py(self.{{ variable.name }}_path,'{{ variable.type }}')
            {% else %}
        return {{ variable.default }}
            {% endif %}

    @irpy.lazy_property_mutable
    def {{ variable.name }}_interface(self):
        return babel.py2interface('{{ variable.type }}',self.{{ variable.name }})

    @irpy.lazy_property
    def {{ variable.name }}_bytes_interface(self):
        return babel.nele2bytes_interface('{{ variable.type }}')


    def set_{{ variable.name }}(self,bytes):

        data_interface = babel.bytes2interface('{{ variable.type }}', bytes)
        self.{{ variable.name }}_interface = data_interface

        zscalar.interface2db(self.{{ variable.name }}_path,self.{{ variable.name }}_interface)

        update_zezfio_id()

        {% else %}

    @irpy.lazy_property_mutable
    def {{ variable.name }}_shape(self):
        return {{variable.dimension}}

    @irpy.lazy_property
    def {{ variable.name }}_nele(self):
        return babel.shape2nele(self.{{ variable.name }}_shape)

    @irpy.lazy_property
    def {{ variable.name }}_path(self):
        return build_path('{{db_path}}','{{ category }}','{{ variable.name }}',array=True)

    @irpy.lazy_property_mutable
    def {{ variable.name }}_interface(self):
        return zarray.db2interface(self.{{variable.name}}_path,'{{ variable.type }}',self.{{ variable.name }}_nele)

    @irpy.lazy_property
    def {{ variable.name }}(self):
        return babel.buffer_interface2py(self.{{ variable.name }}_interface, nele=self.{{ variable.name }}_nele)

    @irpy.lazy_property
    def {{ variable.name }}_bytes_interface(self):
        return babel.nele2bytes_interface('{{ variable.type }}',self.{{ variable.name }}_nele)


    def set_{{ variable.name }}(self,bytes):

        sbytes = len(bytes)
        theobytes = self.{{ variable.name }}_bytes_interface.value

        if  sbytes != theobytes:
            raise IndexError("Conflic between the spec bytes of the array %i and the given one %i" % (sbytes, theobytes))       

        data_interface = babel.bytes2interface('{{ variable.type }}', bytes)
        self.{{ variable.name }}_interface = data_interface

        zarray.interface2db(self.{{ variable.name }}_path,self.{{ variable.name }}_shape,
                            '{{ variable.type }}',self.{{ variable.name }}_interface)

        update_zezfio_id()

        {% endif %}



    {% endfor %}

#For allowing referance in shape
{{ category }} = {{ category|capitalize }}()
#Quicker than getattr
d_instance[ "{{ category }}" ] = {{ category }}

{%  endfor %}
