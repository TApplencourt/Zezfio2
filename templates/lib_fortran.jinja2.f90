subroutine ezfio_set_file(x)
  implicit none
  character*(*) :: x
  call zezfio_initialize()
end

{% for cat, attributes in json_config.iteritems() %}
  {% for var in attributes["attributes"] %}

subroutine ezfio_set_{{cat}}_{{var.name}}(buffer)
   implicit none
   double precision, intent(out) :: buffer(*)
   integer :: zezfio_set, zezfio_size
   integer :: zerrno, buffer_size

   zerrno   = zezfio_size("{{cat}}.{{var.name}}",len("{{cat}}.{{var.name}}"),buffer_size)
   if (zerrno < 0) then
      STOP
   endif

   zerrno = zezfio_set("{{cat}}.{{var.name}}",len("{{cat}}.{{var.name}}"),buffer,buffer_size)
   if (zerrno < 0) then
      STOP
   endif

end subroutine


subroutine ezfio_get_{{cat}}_{{var.name}}(buffer)
   implicit none
   double precision, intent(out) :: buffer(*)
   integer :: zezfio_get
   integer :: zerrno

   zerrno = zezfio_get("{{cat}}.{{var.name}}",len("{{cat}}.{{var.name}}"),buffer)
   if (zerrno < 0) then
      STOP
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