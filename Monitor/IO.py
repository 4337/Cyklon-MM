# -*- coding: utf-8 -*-

import threading 

class IO :

      cnt = 0
      file_handle = { }

      io_lock = threading.Lock( )

      def __init__( self ) :

          pass

      def __del__( self ) :

          if ( IO.cnt > 0 ) :
               if ( len(IO.file_handle) > 0 ):
                    for i in range( 0, len(IO.file_handle) ) :
                        try :
                            if ( i % 2 == 0 ) :
                                 IO.file_handle[i].close( )
                            IO.file_handle.pop( IO.file_handle.keys()[ i ] )
                        except :
                               pass
               else :
                    pass #Hjuston mamy problem : wyjatki w destruktorach sa w przypadku python-a ignorowane - podobno, nadal nie mam zadnej normalnej ksiazki do tego jezyka
          
           IO.cnt = 0

      @staticmethod
      def open_file( file_path, mode ) :
 
          ret = True
          try : 
              IO.io_lock.acquire( True )
              IO.file_handle[file_path] = open( file_path, mode )
              IO.file_handle[IO.cnt] = IO.file_handle[file_path]
              print 'CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC o ' + str( IO.file_handle[file_path] ) + ' ' + str( IO.file_handle[IO.cnt] )
              ++IO.cnt
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
                   print 'WTFGDUWBHGYGB ' + str(data)
                   IO.file_handle[IO.cnt - 1].write( data )
          except Exception as e :
                 print 'LOOKLKLOFKWOKF chodzi ' + str(e)
          finally :
                  IO.io_lock.release( )

      @staticmethod
      def close_file( file_path = '' ) :
          
          try :
              IO.io_lock.acquire( True )
              if ( file_path != '' ) :
                   IO.file_handle[file_path].close( )
              else :   
                   IO.file_handle[IO.cnt - 1].close( )
          
              IO.file_handle.pop( IO.cnt - 1 )
              IO.file_handle.pop( IO.file_handle.keys()[ IO.cnt - 2 ] )
              --IO.cnt
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