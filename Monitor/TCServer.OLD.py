# -*- coding: utf-8 -*-

import socket
import os
import time
import threading

from IO import *
from time import localtime, strftime
from VSystem import *
from VEvent import *

class TCServer : #@@ TODO: change to nonblocking 
 
      Headers = ( "HTTP/1.1 200 OK\r\n"
                  "Server: Apache\r\n"
                  "Content-Type: text/html; charset=utf-8\r\n"
                  "Cache-Control: no-cache, no-store, must-revalidate\r\n"
                  "Connection: Close\r\n" )
                             
      def __set_date( self ) :

          data_time = strftime( "%a, %d %b %Y %H:%M:%S", localtime( ) )
          return "Date: " + str( data_time ) + "\r\n"

      def __set_content_length( self, length ) :

          return "Content-Length: " + str( length ) + "\r\n"

      def __init__( self, bind_addr, bind_port, document_root, f_name ) :

          self.remote_addr = None
          self.addr = bind_addr
          self.port = bind_port
          self.server_socket = None
          self.connect_socket = None 
          self.document_root = document_root 
          self.tc_file = f_name

      def __del__( self ) :

          if ( self.connect_socket != None ) :
               try :
                   self.connect_socket.shutdown( socket.SHUT_RDWR )
               finally :
                       self.connect_socket.close( )
          
          if ( self.server_socket != None ) :
               self.server_socket.close( )


      def listen( self ) :   

          try :
              addr = ( self.addr, int( self.port ) )
              self.server_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
             # self.server_socket.settimeout( 5 )
              self.server_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
              self.server_socket.bind( addr )
              self.server_socket.listen( 1024 )
              return True
          except Exception as e:
                 IO.stdout( 'Socket.listen error ' + str(e) )
                 return False

      def run( self, tc_generator_cmd ) :  #trzeba poprawic

          try :
              IO.stdout( '(*). TC Server->Run() : done !' )
              while ( VEvent.reboot.is_set( ) == False ) :
        
                      try :
                          ( self.connect_socket, self.remote_addr ) = self.server_socket.accept( )  
                          self.connect_socket.recv( 4096 )
                          os.popen( tc_generator_cmd ).read( )  #fix : white space in command 
                          f_name = self.document_root + '\\' + self.tc_file
                          f = open( f_name )
                          test_case = f.read( )
                          f.close( )
                          response = ( self.Headers + self.__set_date( ) + 
                                       self.__set_content_length( len( test_case ) ) + "\r\n" + 
                                       test_case )
                          self.connect_socket.sendall( response )
                          self.connect_socket.shutdown( socket.SHUT_RDWR )
                          self.connect_socket.close( ) 
                          self.connect_socket = None
                      except Except as e:  
                             IO.stdout( ' except in socket ' + str(e) )
                             self.connect_socket.shutdown( socket.SHUT_RDWR )
                             self.connect_socket.close( )
                             self.connect_socket = None

              return True
          except :
                 return False