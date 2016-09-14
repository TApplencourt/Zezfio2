module zezfio
   implicit none
   private
   public :: f77_zmq_ctx_new, f77_zmq_socket, f77_zmq_connect, &
      f77_zmq_close, f77_zmq_ctx_destroy,               &
      f77_zmq_send, f77_zmq_recv,                       &
      ZMQ_REQ, ZMQ_PTR,ZMQ_SNDMORE,                     &
      context,responder

   include 'f77_zmq.h'
   integer(ZMQ_PTR) :: context
   integer(ZMQ_PTR) :: responder

end module

subroutine zezfio_initialize(address)
   use zezfio, only: f77_zmq_ctx_new, f77_zmq_socket, f77_zmq_connect, &
      context, responder, ZMQ_REQ
   implicit none

   character*(128), optional       :: address
   integer                         :: rc

   if (.not.present(address)) then
      call getenv("ZEZFIO_ADDRESS", address)
      if ( len_trim(address) == 0 ) then
          print*, "Please source $ZEZFIO_ADDRESS enviroment variable"
          STOP 1
      endif
   endif

   context   = f77_zmq_ctx_new()
   responder = f77_zmq_socket(context, ZMQ_REQ)
   rc        = f77_zmq_connect(responder,address)

   if ( rc == -1 ) then
      print*, "Cannot connect to the server located at ",address
      STOP 1
   endif

end subroutine zezfio_initialize


subroutine zezfio_finalize()
   use zezfio, only: f77_zmq_close, f77_zmq_ctx_destroy, responder, context
   implicit none

   integer  ::  rc

   rc = f77_zmq_close(responder)
   rc = f77_zmq_ctx_destroy(context)

end subroutine zezfio_finalize

function zezfio_has(msg,msg_size) result(zerrno)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, responder
   implicit none

   integer,              intent(in) :: msg_size
   character*(msg_size), intent(in) :: msg
   integer                          :: zerrno
   integer                          :: rc

   rc = f77_zmq_send(responder, "has."//msg, 4+msg_size,0)
   rc = f77_zmq_recv(responder,  zerrno,     4,         0)

end function zezfio_has


function zezfio_get(msg,msg_size,ptr_buffer) result(zerrno)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, responder, ZMQ_PTR
   implicit none

   integer                      :: rc

   integer,              intent(in) :: msg_size
   character*(msg_size), intent(in) :: msg
   integer                          :: zerrno
   integer(ZMQ_PTR), intent(out)    :: ptr_buffer
   integer                          :: buffer_size

   rc = f77_zmq_send(responder, "get."//msg, 4+msg_size,0)
   rc = f77_zmq_recv(responder,zerrno,4, 0)
   
   if (zerrno >= 0) then

      rc = f77_zmq_recv(responder, buffer_size,          4, 0)
      rc = f77_zmq_recv(responder, ptr_buffer, buffer_size, 0)
   endif

end function zezfio_get

function zezfio_set(msg,msg_size,ptr_buffer,buffer_size) result(zerrno)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, responder, ZMQ_PTR, ZMQ_SNDMORE
   implicit none

   integer                      :: rc

   integer,              intent(in) :: msg_size
   character*(msg_size), intent(in) :: msg
   integer(ZMQ_PTR),     intent(in) :: ptr_buffer
   integer,              intent(in) :: buffer_size
   integer                          :: zerrno

   rc = f77_zmq_send(responder, "set."//msg, 4+msg_size,  ZMQ_SNDMORE)
   rc = f77_zmq_send(responder, ptr_buffer,  buffer_size, 0)

   rc = f77_zmq_recv(responder,zerrno,4, 0)

end function zezfio_set

function zezfio_nbytes(msg,msg_size,buffer_size) result(zerrno)
   use zezfio, only: f77_zmq_send, f77_zmq_recv, responder, ZMQ_PTR, ZMQ_SNDMORE
   implicit none

   integer                      :: rc

   integer,              intent(in)  :: msg_size
   character*(msg_size), intent(in)  :: msg
   integer,              intent(out) :: buffer_size
   integer                           :: zerrno

   rc = f77_zmq_send(responder, "size."//msg, 5+msg_size,  0)

   rc = f77_zmq_recv(responder,zerrno,4, 0)
   rc = f77_zmq_recv(responder,buffer_size,4, 0)

end function zezfio_nbytes
