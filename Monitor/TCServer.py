# -*- coding: utf-8 -*-

import os
import SocketServer

from BaseHTTPServer import HTTPServer

from BaseHTTPServer import BaseHTTPRequestHandler

from IO import *
from VSystem import *
from VEvent import *

class TCServer :

      CMD = ''
      DOCUMENT_ROOT = '' 
      TC_FILE = ''

      class __handler( BaseHTTPRequestHandler ) : 
         
         def handle_error( self, request, client_address ) :

             IO.stdout('[!]. TCServer.handle_error() error !')

         def __sh( self ) :
             
             self.send_response( 200 )
             self.send_header( 'Content-type', 'text/html' )
             self.end_headers( )

         def __handle( self ) :

             os.popen( TCServer.CMD ).read( ) 

             f = open( TCServer.DOCUMENT_ROOT + '\\' + TCServer.TC_FILE )
             test_case = f.read( )
             f.close( )

             return test_case        

         def do_GET( self ) :
             try :
                  self.__sh( )
                  tc = self.__handle( )
                  self.wfile.write( tc )
             except :
                    pass 
         
         def do_POST( self ) :
             try :
                 self.__sh( )
                 tc = self.__handle( )
                 self.wfile.write( tc )
             except :
                    pass

         def log_message(self, format, *args) : 
             return

      def __init__( self, bind_addr, bind_port, document_root, f_name, cmd ) :

           self.server = None
           self.addr = bind_addr
           self.port = int( bind_port )
           TCServer.DOCUMENT_ROOT = document_root 
           TCServer.TC_FILE = f_name
           TCServer.CMD = cmd


      def __del__( self ) :

          if ( self.server != None ) :

               self.server.shutdown( )
               #self.server = None
               

      def listen( self ) :
 
          try : 
               SocketServer.TCPServer.allow_reuse_address = True
               self.server = HTTPServer(( self.addr, self.port ), self.__handler )
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

 

