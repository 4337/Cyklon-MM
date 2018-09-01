# -*- coding: utf-8 -*-

import threading 

class IO :

      cnt = 0
      file_handle = [ ]

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
              IO.file_handle.append( { 'name' : open( file_path, mode ), 'handle' : file_path } )
              ++IO.cnt
          except Exception as e :
                 ret = False
          finally :
                  IO.io_lock.release( )
                  return ret
       
      @staticmethod
      def write_file( data, file_path = '' ) :
          IO.io_lock.acquire( True )
          if ( file_path != '' ) :
               for o in IO.file_handle :
                   if ( file_path in o['name'] ) :
                        o['handle'].write( data )
          else : 
                IO.file_handle[IO.cnt - 1]['handle'].write( data )
          IO.io_lock.release( )

      @staticmethod
      def close_file( file_path = '' ) :
          
          IO.io_lock.acquire( True )
          if ( file_path != '' ) :
               for o in IO.file_handle :
                   if ( file_path in o['handle'] ) :
                        o['handle'].close( )
          else :   
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