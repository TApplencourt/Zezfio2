subroutine ezfio_set_file(x)
  implicit none
  character*(*) :: x
  call zezfio_initialize(x)
end

{% for cat, attributes in json_config.iteritems() %}
  {% for var in attributes["attributes"] %}

subroutine ezfio_set_{{cat}}_{{var.name}}(buffer)
   implicit none
   {{ c2stuff[var.type].fortran_type }}, intent(in) :: buffer(*)
   integer :: zezfio_set, zezfio_nbytes
   integer :: zerrno, buffer_size

   zerrno   = zezfio_nbytes("{{cat}}.{{var.name}}",len("{{cat}}.{{var.name}}"),buffer_size)
   if (zerrno < 0) then
      print *,  'Errno < 0 in ezfio_set_{{cat}}_{{var.name}}: zezfio_nbytes'
      STOP -1
   endif

   zerrno = zezfio_set("{{cat}}.{{var.name}}",len("{{cat}}.{{var.name}}"),buffer,buffer_size)
   if (zerrno < 0) then
      print *,  'Errno < 0 in ezfio_set_{{cat}}_{{var.name}}: zezfio_set'
      STOP -1
   endif

end subroutine


subroutine ezfio_get_{{cat}}_{{var.name}}(buffer)
   implicit none
   {{ c2stuff[var.type].fortran_type }}, intent(out) :: buffer(*)
   integer :: zezfio_get
   integer :: zerrno

   zerrno = zezfio_get("{{cat}}.{{var.name}}",len("{{cat}}.{{var.name}}"),buffer)
   if (zerrno < 0) then
      print *,  'Errno < 0 in ezfio_get_{{cat}}_{{var.name}}: zezfio_get'
      STOP -1
   endif

end subroutine

subroutine ezfio_has_{{cat}}_{{var.name}}(has_it)

   implicit none

   logical, intent(out) :: has_it
   integer :: zezfio_has
   integer :: zerrno

   zerrno = zezfio_has("{{cat}}.{{var.name}}",len("{{cat}}.{{var.name}}"))
   if (zerrno < 0) then
      has_it = .FALSE.
   else
      has_it = .TRUE.
   endif

end subroutine
  {% endfor %}
{% endfor %}
