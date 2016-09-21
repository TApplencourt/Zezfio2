module zezfio
   implicit none
   private
   public :: f77_zmq_ctx_new, f77_zmq_socket, f77_zmq_connect, &
      f77_zmq_close, f77_zmq_ctx_destroy,               &
      f77_zmq_send, f77_zmq_recv,                       &
      ZMQ_REQ, ZMQ_PTR,ZMQ_SNDMORE,                     &
      context,requester

   include 'f77_zmq.h'
   integer(ZMQ_PTR) :: context
   integer(ZMQ_PTR) :: requester

end module

subroutine zezfio_initialize(address)
   use zezfio, only: f77_zmq_ctx_new, f77_zmq_socket, f77_zmq_connect, &
      context, requester, ZMQ_REQ
   implicit none

   character(len=*), intent(in)    :: address
   character*(128)                 :: ezfio_address
   integer                         :: rc

   if (len_trim(address) == 0 ) then
      call getenv("ZEZFIO_ADDRESS", ezfio_address)
      if ( len_trim(ezfio_address) == 0 ) then
          print*, "Please set the ZEZFIO_ADDRESS enviroment variable"
          STOP 1
      endif
   else
      ezfio_address = address
   endif

   context   = f77_zmq_ctx_new()
   requester = f77_zmq_socket(context, ZMQ_REQ)
   rc        = f77_zmq_connect(requester,ezfio_address)

   if ( rc == -1 ) then
      print*, "Cannot connect to the server located at ",ezfio_address
      STOP 1
   endif

end subroutine zezfio_initialize


subroutine zezfio_finalize()
   use zezfio, only: f77_zmq_close, f77_zmq_ctx_destroy, requester, context
   implicit none

   integer  ::  rc

   rc = f77_zmq_close(requester)
   rc = f77_zmq_ctx_destroy(context)

end subroutine zezfio_finalize

function zezfio_has(msg) result(has_it)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, requester
   implicit none

   character*(*), intent(in)        :: msg
   integer                          :: zerrno
   integer                          :: rc
   logical                          :: has_it

   rc = f77_zmq_send(requester, "has."//msg, 4+len(msg),0)
   rc = f77_zmq_recv(requester,  zerrno,     4,         0)

   has_it = (rc >= 0)

end function zezfio_has


function zezfio_get(msg,ptr_buffer) result(zerrno)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, requester, ZMQ_PTR
   implicit none

   integer                      :: rc

   character*(*), intent(in)        :: msg
   integer                          :: zerrno
   integer(ZMQ_PTR), intent(out)    :: ptr_buffer
   integer                          :: buffer_size

   rc = f77_zmq_send(requester, "get."//msg, 4+len(msg),0)
   rc = f77_zmq_recv(requester,zerrno,4, 0)

   
   if (zerrno >= 0) then

      rc = f77_zmq_recv(requester, buffer_size,          4, 0)
      rc = f77_zmq_recv(requester, ptr_buffer, buffer_size, 0)
   endif

end function zezfio_get

function zezfio_set(msg,ptr_buffer,buffer_size) result(zerrno)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, requester, ZMQ_PTR, ZMQ_SNDMORE
   implicit none

   integer                      :: rc

   character*(*)   ,     intent(in) :: msg
   integer(ZMQ_PTR),     intent(in) :: ptr_buffer
   integer,              intent(in) :: buffer_size
   integer                          :: zerrno

   rc = f77_zmq_send(requester, "set."//msg, 4+len(msg),  ZMQ_SNDMORE)
   rc = f77_zmq_send(requester, ptr_buffer,  buffer_size, 0)

   rc = f77_zmq_recv(requester,zerrno,4, 0)

end function zezfio_set

function zezfio_nbytes(msg,buffer_size) result(zerrno)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, requester, ZMQ_PTR, ZMQ_SNDMORE
   implicit none

   integer                      :: rc

   character*(*),        intent(in)  :: msg
   integer,              intent(out) :: buffer_size
   integer                           :: zerrno

   rc = f77_zmq_send(requester, "size."//msg, 5+len(msg),  0)

   rc = f77_zmq_recv(requester,zerrno,4, 0)

   if (zerrno >= 0) then
     rc = f77_zmq_recv(requester,buffer_size,4, 0)
   endif

end function zezfio_nbytes
