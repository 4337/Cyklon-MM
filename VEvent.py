# -*- coding: utf-8 -*-

import threading

class VEvent :
      
      '''
      jesli nie sygnalizowany restartuj 
      '''
      no_freeze = threading.Event( )
      no_freeze.set( )

      '''
      zdarzenie jest sygnalizowane przez watchdoga po uplynieciu czasu sesji 
      oraz przez instacje Dbg po wykryciu interesujacych wyjatkow
      sygnalizuje watka App oraz Server ze maja zakonczyc dzialenie 
      '''
      reboot = threading.Event( )
      '''
      zdarzenie jest zapalane przez instanjce Dbg po tym 
      jak debugger zostanie podlaczony do aplikacji i uruchomi glowna petle.
      jest to znak dla innych watkow (instancji App i WatchDog) ze moga realizowac swoje zadania 
      (przekierowanie do stron, etc)
      '''
      dbg_ready = threading.Event( )

      def __init__( self ) :
           
          pass

      def __del__( slef ) :
      
          print "[x]. In VEvent.__del__() !\r\n"
       