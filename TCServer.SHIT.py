# -*- coding: utf-8 -*-

import os
import SocketServer

from time import localtime, strftime

from IO import *
from VSystem import *
from VEvent import *

class TCServer :

      CMD = ''
      DOCUMENT_ROOT = '' 
      TC_FILE = ''
      REQUEST_COUNT = 0

      HEADERS = ( "HTTP/1.1 200 OK\r\n"
                  "Server: Apache\r\n"
                  "Content-Type: text/html; charset=utf-8\r\n"
                  "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                  "Connection: Close\r\n" )

      class __handler( SocketServer.BaseRequestHandler ) : 

      
         def __set_date( self ) :

             data_time = strftime( "%a, %d %b %Y %H:%M:%S", localtime( ) )
             return "Date: " + str( data_time ) + "\r\n"

         def __set_content_length( self, length ) :

             return "Content-Length: " + str( length ) + "\r\n"

         def handle( self ) :
     
             TCServer.REQUEST_COUNT = TCServer.REQUEST_COUNT + 1;
             self.request.recv( 1024 )
             tc = self.__handle( )
             rsp = ( TCServer.HEADERS + self.__set_date( ) + 
                     self.__set_content_length( len( tc ) ) + "\r\n" + 
                     tc )
             self.request.sendall( rsp )
         
         def handle_error( self, request, client_address ) :

             IO.stdout('[!]. TCServer.handle_error() error !')
             return

         def __handle( self ) :

             os.popen( TCServer.CMD ).read( ) 

             f = open( TCServer.DOCUMENT_ROOT + '\\' + TCServer.TC_FILE )
             test_case = f.read( )
             f.close( )

             return test_case        

         def log_message(self, format, *args) : 
             return

      def __init__( self, bind_addr, bind_port, document_root, f_name, cmd ) :

           self.server = None
           self.addr = bind_addr
           self.port = int( bind_port )
           TCServer.DOCUMENT_ROOT = document_root 
           TCServer.TC_FILE = f_name
           TCServer.CMD = cmd
           TCServer.REQUEST_COUNT = 0


      def __del__( self ) :

          if ( self.server != None ) :
               try :
                    self.server.shutdown( )
               except :
                      pass
               self.server.server_close( )
               #TCServer.REQUEST_COUNT = 0
               #self.server = None
               

      def listen( self ) :
 
          try : 
               SocketServer.TCPServer.allow_reuse_address = True
               self.server = SocketServer.TCPServer(( self.addr, self.port ), self.__handler )
               SocketServer.TCPServer.allow_reuse_address = True
               return True
          except Exception as e:
                  return False

      def run( self ) :

              try :
                   while ( VEvent.reboot.is_set( ) == False ) :
                           self.server.handle_request( ) #.serve_forever( ) 
                   return True
              except Exception as e:
                     return False

 

