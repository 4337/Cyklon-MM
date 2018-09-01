# -*- coding: utf-8 -*-

import psutil
import threading 
import VEvent 
import time 
import tempfile

from IO import *
from VEvent import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class App :

      pids = []
      hang_time_out = 25 #page hang x seconds
      load_time_out = 20 #page load y seconds

      def __init__( self, path, file_name, cmd ) :
   
          self.path = path
          self.browser = None
          self.cmd_line = cmd #addr
          self.additional_apps = []
          self.loop_exit_result = False
          self.app_file = file_name
          pass

      def __del__( self ) :

          del App.pids[:]
          if ( self.browser != None ) :
               try :
                   self.browser.quit( )
                   del self.browser
               except :
                      pass 

      def __get_drv( self, app ) :

          temp_dir = tempfile.gettempdir( )
          name = app.split( '.' )[0]
          
          if ( 'firefox' in name.lower( ) ) :
                caps = DesiredCapabilities.FIREFOX
                try : 
                     prv = webdriver.FirefoxProfile( )
                     prv.set_preference( 'browser.download.folderList', 2)
                     prv.set_preference( 'browser.download.dir', temp_dir + '\Default' )
                     drv = webdriver.Firefox( firefox_profile = prv )  #CHCK !
                     return drv
                except Exception as e:
                       return None
          if ( 'edge' in name.lower( ) ) :  # ## MicrosoftEdge.exe
                self.additional_apps.extend( ['browser_broker.exe','RuntimeBroker.exe','ApplicationFrameHost.exe','MicrosoftEdgeCP.exe'] )
                caps = DesiredCapabilities.EDGE
                return webdriver.Edge( )
          if ( 'chrome' in name.lower( ) ) :
                caps = DesiredCapabilities.CHROME
                return webdriver.Chrome( )
          if ( 'iexplore' in name.lower( ) ) :  #Achtung : disable protected mode for all zones in IE, otherway selenium will throw exception
		caps = DesiredCapabilities.INTERNETEXPLORER
                caps['ignoreZoomSetting'] = True
                return webdriver.Ie( capabilities = caps )
 
          return None

      def run( self ) :

          try : 

              self.browser = self.__get_drv( self.app_file )     
              if ( self.browser == None ) :
                   return False   
              self.browser.set_page_load_timeout( App.hang_time_out )  
              self.browser.get( 'about:blank' )

              for proc in psutil.process_iter( attrs = ['name','pid'] ) :
                  if ( self.app_file.lower( ) in proc.info['name'].lower( ) ) :
                       App.pids.append( proc.info['pid'] )
                  for app in self.additional_apps :
                      if ( app.lower( ) in proc.info['name'].lower( ) ) :
                           self.pids.append( proc.info['pid'] )
    
              IO.stdout( "(*). Application |" + self.app_file + "| start (wait for dbg) : done !" )
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