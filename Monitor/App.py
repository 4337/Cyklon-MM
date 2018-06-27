# encoding=utf8

import psutil
import threading 
import VEvent 
import time 

from IO import *
from VEvent import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class App :

      pids = []
      hang_time_out = 15 #page hang 15 seconds
      load_time_out = 10 #page load 10 seconds

      def __init__( self, path, file_name, cmd ) :
   
          self.path = path
          self.browser = None
          self.cmd_line = cmd #addr
          self.additional_apps = []
          self.loop_exit_result = False
          self.app_name = self.__set_app_name( file_name )
          pass

      def __del__( self ) :

          del App.pids[:]
          if ( self.browser != None ) :
               try :
                   self.browser.quit( )
                   del self.browser
               except :
                      pass 

      def __set_app_name( self, app ) :

          name = app.split( '.' )[0]
          
          if ( 'firefox' in name.lower( ) ) :
                return 'Firefox'
          if ( 'edge' in name.lower( ) ) :
                self.additional_apps.extend( ['browser_broker.exe','RuntimeBroker.exe','ApplicationFrameHost.exe'] )
                return 'Edge'
          if ( 'chrome' in name.lower( ) ) :
                return 'Chrome'
          if ( 'iexplore' in name.lower( ) ) :
                return 'Ie'
 
          return None

      def run( self ) :

          try : 

              selenium = getattr( webdriver, self.app_name )
              self.browser = selenium( )
              self.browser.set_page_load_timeout( App.hang_time_out )  
              self.browser.get( 'about:blank' )

              for proc in psutil.process_iter( attrs = ['name','pid'] ) :
                  if ( self.app_name.lower( ) in proc.info['name'].lower( ) ) :
                       App.pids.append( proc.info['pid'] )
                  for app in self.additional_apps :
                      if ( app.lower( ) in proc.info['name'].lower( ) ) :
                           self.pids.append( proc.info['pid'] )
    
              IO.stdout( "(*). Application |" + self.app_name + "| start (wait for dbg) : done !" )
              return True

          except Exception as e :
                 print 'App.run() exception ' + str(e)
                 return False

      def go( self ) : #thread

          VEvent.dbg_ready.wait( )
          IO.stdout( '(*). App [dbg ready] App.go() working !' )

          while ( VEvent.reboot.is_set( ) == False ) :
                  try :
                      self.browser.get( self.cmd_line )
                      try :
                          WebDriverWait(self.browser, App.load_time_out).until(EC.presence_of_element_located( (By.TAG_NAME, "body") ) )
                      except Exception as e: 
                             pass
                      time.sleep( 1 )
                  except Exception as e:
                         VEvent.reboot.set( )
                         self.loop_exit_result = False
    
          self.loop_exit_result = True