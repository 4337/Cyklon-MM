# -*- coding: utf-8 -*-

import os
import threading 

class IO :

      cnt = 0
      file_handle = { }

      io_lock = threading.Lock( )

      def __init__( self ) :

          pass

      def __del__( self ) :

          t_cnt = len(IO.file_handle)

          if ( IO.cnt == t_cnt  ) :
               if ( t_cnt > 0 ):
                    IO.cnt = 0
                    for i in range( 0, t_cnt ) :
                        try :
                            IO.file_handle[IO.file_handle.keys()[i]].close( )
                            IO.file_handle.pop( IO.file_handle.keys()[ i ] )
                        except Exception as e :
                               pass
          else :
                pass #Hjuston mamy problem : wyjatki w destruktorach sa w przypadku python-a ignorowane - podobno, nadal nie mam zadnej normalnej ksiazki do tego jezyka

      @staticmethod
      def open_file( file_path, mode ) :
 
          ret = True
          try : 
              IO.io_lock.acquire( True )
              IO.file_handle[file_path] = open( file_path, mode ) #0 -> 'key'
              IO.cnt = IO.cnt + 1
          except Exception as e :
                 ret = False
          finally :
                  IO.io_lock.release( )
                  return ret
       
      @staticmethod
      def write_file( data, file_path = '' ) :
          try : 
              IO.io_lock.acquire( True )
              if ( file_path != '' ) :
                   IO.file_handle[file_path].write( data )
              else : 
                   IO.file_handle[ IO.file_handle.keys()[IO.cnt - 1] ].write( data )
          except Exception as e :
                 pass
          finally :
                  IO.io_lock.release( )

      @staticmethod
      def close_file( file_path = '' ) :
          
          try :
              IO.io_lock.acquire( True )
              if ( file_path != '' ) :
                   IO.file_handle[file_path].close( )
                   IO.file_handle.pop( file_path )
              else :   
                   IO.file_handle[IO.file_handle.keys()[IO.cnt - 1]].close( )
                   IO.file_handle.pop( IO.file_handle.keys()[IO.cnt - 1] )
              IO.cnt = IO.cnt - 1
          finally :
                  IO.io_lock.release( )

      @staticmethod
      def stdout( msg ) :
          
          try :
              IO.io_lock.acquire( True )
              print msg
          finally :
                  IO.io_lock.release( )
                  return msg + "\r\n"

      @staticmethod
      def __lock__() :

          try :
               hnd = open('.lock','w')
               hnd.write('lockme')
               hnd.close()
          except :
                  pass

      @staticmethod
      def __unlock__() :
          
          os.remove('.lock')