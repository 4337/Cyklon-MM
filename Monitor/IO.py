# -*- coding: utf-8 -*-

import threading 

class IO :

      cnt = 0
      file_handle = []

      io_lock = threading.Lock( )

      def __init__( self ) :

          pass

      def __del__( self ) :

          pass

      @staticmethod
      def open_file( file_path, mode ) :
 
          ret = True
          try : 
              IO.io_lock.acquire( True )
              IO.file_handle.append( open( file_path, mode ) )
              ++IO.cnt
          except Exception as e :
                 ret = False
          finally :
                  IO.io_lock.release( )
                  return ret
       
      @staticmethod
      def write_file( data ) :
          IO.io_lock.acquire( True )
          IO.file_handle[IO.cnt - 1].write( data )
          IO.io_lock.release( )

      @staticmethod
      def close_file( ) :
          
          IO.io_lock.acquire( True )
          IO.file_handle[IO.cnt - 1].close( )
          IO.file_handle.pop( IO.cnt - 1 )
          --IO.cnt
          IO.io_lock.release( )

      @staticmethod
      def stdout( msg ) :

          IO.io_lock.acquire( True )
          try :
               print msg
          except : 
                 pass
          IO.io_lock.release( )
          return msg + "\r\n"