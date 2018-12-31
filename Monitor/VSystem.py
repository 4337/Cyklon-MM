# -*- coding: utf-8 -*-

import os
import time
import shutil
import ctypes
import _winreg
import VEvent
import threading 
import winappdbg
import warnings

from IO import *
from App import *
from Dbg import *
from VEvent import *
from Utils import *
from TCServer import *
from urlparse import urlparse
from time import localtime, strftime

class VSystem :

      dbg_reboot_on_error = False

      '''
      Watki ;)
      '''
      threads = [] 

      '''
      /************************************************************************
      *  timer
      *************************************************************************/
      '''
      class WatchDog :

            def __init__( self ) :
                self.timeo = 0
 
            def __watch( self ) :

                VEvent.dbg_ready.wait( )
                VEvent.reboot.wait( float(self.timeo) )

                VEvent.no_freeze.wait( )

                IO.stdout( '(*). [' + strftime( "%d/%m/%Y %H:%M:%S", localtime( ) ) + '] System reboot !' )

                if ( VEvent.reboot.is_set( ) == False ) :
                     VEvent.reboot.set( )

            def run( self, time_o ) :
 
                try :
                    self.timeo = time_o

                    th = threading.Thread( target = self.__watch )
                    VSystem.threads.append( th )
                    th.start( )

                    IO.stdout( '(*). [' + strftime( "%d/%m/%Y %H:%M:%S", localtime( ) ) + '] Watchdog start with time ' + str(self.timeo / 60) + ' minutes (wait for dbg) : done !' )

                    return True
                except :
                       return False
      
      '''
      ## end timer #############################################################
      '''
     
      '''
      /*************************************************************************
       * @@private __chck_env : set PATH variables 
       *************************************************************************
      '''
      def __chck_env( self, set = True ) :  

	  __env = ''
          ret = True
          sub_d = os.listdir( self.cwd + self.cfg['drivers_dir']  )

          if ( len( sub_d ) <= 0 ) : 
               return False 

          key_hnd = ['',''];
          keys = [ { 'key': _winreg.HKEY_LOCAL_MACHINE, 's_key': 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment' },
                   { 'key': _winreg.HKEY_CURRENT_USER, 's_key': 'Environment' } ]

          for dir in sub_d : 

              drv_path = self.cwd + self.cfg['drivers_dir'] + '\\' + dir

              for i in range( len( keys ) ) :            #optymalniej byloby gdby ta byla nadrzedna wzgledem dir in sub_d, ale chooj nie chce mi sie ;/

		  key_hnd[i] =  _winreg.CreateKey( keys[i]['key'], keys[i]['s_key'] ) 
		  
                  if ( not key_hnd[i] ) :
                       ret = False
                  else :
                        try : 
                             __env = _winreg.QueryValueEx( key_hnd[i], 'PATH' )
                        except :
                               ret = False
                         
                        if ( len( __env ) > 0 ) :    
                            
                             if ( __env[0].endswith( ';' ) ) :
                                  c__env = __env[0] + os.path.abspath( drv_path ) + ';'
                             else : 
                                  c__env = __env[0] + ';' + os.path.abspath( drv_path )
                        
                             if ( os.path.abspath( drv_path ) not in __env[0] ) :

                                  if ( set == True ) :

                                       try :
                                           _winreg.SetValueEx( key_hnd[i], 'PATH', 0, _winreg.REG_EXPAND_SZ, c__env )
                                       except Exception as e :
                                                             ret = False

                                  else : 
                                       ret = False
 
                             if ( os.path.abspath( drv_path ) not in os.environ['PATH'] ) :
                                 
                                  os.environ['PATH'] = c__env.encode( 'ascii', 'ignore' ) 

                  key_hnd[i].Close( )
                 
          if ( ret != False ) :
               ctypes.windll.user32.SendMessageA( 0xFFFF, 0x1A, 0, 'Environment' )
                   
          return ret
 
      '''
      ### end __chck_env ########################################################
      '''
 
      @staticmethod
      def request_dbg_privileges( ) :

          return winappdbg.System.request_debug_privileges( )

      def stop_drivers( self ) :

          drv_path = os.path.abspath( self.cwd + self.cfg['drivers_dir'] )

          for root, dirs, files in os.walk( drv_path ) :
              for proc in psutil.process_iter( attrs = ['name','pid'] ) :
                  if ( str( files ) == "['" + proc.info['name'] + "']" ) :
                       try :
                           psutil.Process( int( proc.info['pid'] ) ).kill( )
                           IO.stdout('(*). VSystem stop driver (' + str( proc.info['pid'] ) +') : done !' )
                       except Exception as e: 
                              pass
 
      def __init__( self ) :
          
          self.cfg = None
          self.app = None
          self.dbg = None
          self.server = None
          self.cfg_path = None
          self.cmd_line = None #command line options UI->ParseCommandLine
          self.cwd = os.path.dirname( os.path.realpath( __file__ ) ) + "\\"

          warnings.filterwarnings( "ignore" )

          if ( os.path.isfile( self.cwd + "Config.ini" ) == True ) :
               self.cfg_path = self.cwd + "Config.ini" 

          self.watch_dog = self.WatchDog( )
   
      def __del__( self ) :

         for th in VSystem.threads :
             if ( th.is_alive( ) == True ) :
                  ctypes.pythonapi.PyThreadState_SetAsyncExc(  ctypes.c_long( th.ident ), ctypes.py_object( SystemExit ) ) 

         if ( self.app != None ) :
              del self.app
         if ( self.server != None ) :
              del self.server
         if ( self.dbg != None ) :
              del self.dbg

      '''
      /*******************************************************************************************
       * Start and stop application methods :
       *    stop_app( self ) - stop app thread and end selenium session
       *    start_app( self ) - create App instace, run selected browser with about:blank address,
       *                        run realoading thread 
       *******************************************************************************************/
      '''
      def stop_app( self, silent = False ) :
   
          if ( VEvent.reboot.is_set( ) == False ) :
               VEvent.reboot.set( )

          if ( silent == False ) :
               IO.stdout( '(*). App stop' )

          self.stop_drivers( )
          del self.app
          self.app = None

      def run_app( self ) :

          try :
              self.app = App( self.cfg['app_path'], self.cfg['app_name'], self.cfg['tc_url'] )
              if ( self.app.run( ) != True ) :
                   return False
              try : 
                  th = threading.Thread( target = self.app.go )
                  th.start( )
                  VSystem.threads.append( th )
                  return True
              except Exception as e:
                     return False
          except Exception as e:
                 return False

          return True
      '''
      ## end of App (start and stop) ##############################################################
      '''

      '''
      /********************************************************************************************
       * Start and stop tc server methods:
       *    start_tc_server( self ) - start testcase server 
       *    stop_tc_server( self ) - stop testcase server
       ********************************************************************************************/
      '''
      def start_tc_server( self ) :
          
          try : 
              gen_cmd = self.cfg['tc_tec'] + ' ' + self.cwd + self.cfg['tc_generator'] + ' ' + self.cwd + self.cfg['tc_command']
              tc_url = urlparse( self.cfg['tc_url']  ).netloc.split(':')[0]
              self.server = TCServer( tc_url, self.cfg['server_port'] , self.cwd + self.cfg['server_dir'], self.cfg['tc_file'] )

              if ( self.server.listen( ) == True ) :
                   IO.stdout( '(*). TC server listen on addr |' + tc_url + '| port |' + str( self.cfg['server_port'] ) + '| : done !' )
                   th = threading.Thread( target = self.server.run, args = [gen_cmd] )
                   VSystem.threads.append( th ) 
                   th.start( )
                   return True

              return False
          except Exception as e:
                 return False

      def stop_tc_server( self, silent = False ) :
    
          if ( silent == False ) :
               IO.stdout( '(*). TC Server stop' )

          if ( VEvent.reboot.is_set( ) == False ) :
               VEvent.reboot.set( )

          del self.server
          self.server = None

      '''
      ## end of TCServer methods ###################################################################
      '''

      '''
      /*********************************************************************************************
       * Start dbg methods :
       *  dbg_start - attach dbg to all application processes and run dbg loop
       *  dbg_stop  - stop dbg
       *********************************************************************************************/
      '''
      def dbg_start( self, anty_dbg ) :

          if ( self.cfg['dbg_symbols_url'] != None ) :
               sym_url = self.cfg['dbg_symbols_url']
          else :
               sym_url = self.cfg['def_sym']
          
          Dbg.set_symbol_path( sym_url, self.cwd + self.cfg['symbols_dir'] )
          Dbg.set_symbol_reload( self.cfg['reboot_time'] )

          self.dbg = Dbg( os.path.abspath( self.cwd + self.cfg['symbols_dir'] ) , anty_dbg, VSystem.dbg_reboot_on_error, self.cfg['dbghelp'] ) 
          if ( self.dbg.attach_multi( App.pids ) == False ) : 
               return False
          try :
              self.dbg.run( )
              return True
          except Exception as e:
                 return False

      def dbg_stop( self, silent = False ) :
          
          if ( silent == False ) :
               IO.stdout( '(*). Dbg stop ' )

          if ( self.dbg != None ) :
               self.dbg.stop( )
               del self.dbg
               self.dbg = None

      '''
      ## end of dbg ################################################################################
      '''

      '''
      /*********************************************************************************************
       * Start log method : addon 28.05.2018
       *********************************************************************************************/
      '''
      def log( self, msg ) :

               date = strftime( "%d-%m-%Y_%H%M%S", localtime( ) )
               name = self.cwd + self.cfg['repos_dir'] + '\\' + self.cfg['app_name'].split( '.' )[0] + '-' + date + '-' + Dbg.crsh_signature 

               if ( IO.open_file( name + '.crsh', 'w' ) != True ) :
                    return False
               
               IO.write_file( Dbg.exception_info )
               IO.close_file( )
               
               shutil.copy( self.cwd + self.cfg['server_dir'] + '\\' + self.cfg['tc_file'], name + '.html' )

               return True

      '''
      #### end log method   #########################################################################
      '''

      def clear_events( self ) :

          if ( VEvent.dbg_ready.is_set( ) == True ) :
               VEvent.dbg_ready.clear( )
          if ( VEvent.reboot.is_set( ) == True ) :
               VEvent.reboot.clear( )
          if ( VEvent.no_freeze.is_set( ) == False ) :
               VEvent.no_freeze.set( )

      def set_cmdopt( self, cmd ) :
          
          self.cmd_line = cmd
          return cmd

      def chck_evn( self, cfg, install = True ) :

          mk_dirs = [ 'symbols_dir', 'server_dir', 'repos_dir' ] 

          if ( (os.path.isfile( self.cwd + cfg['tc_generator']) != True ) or 
               (os.path.isdir( self.cwd + cfg['drivers_dir']) != True ) ) :
                return False
          else :
               drv_s_dir = [ 'CHROME', 'IE32', 'IE64', 'FF32', 'FF64', 'MSEDGE', 'OPERA32', 'OPERA64' ]
               for subd in drv_s_dir :
                   if ( os.path.isdir( self.cwd + cfg['drivers_dir'] + '\\' + subd ) != True ) :
                        if ( install == True ) :
                             try :
                                 os.makedirs( self.cwd + cfg['drivers_dir'] + '\\' + subd ) 
                             except :
                                  return False
                        else :
                             return False
                                 
          for dir in mk_dirs  :
              if ( os.path.isdir( self.cwd + cfg[dir] ) != True ) :
                   if ( install == True ) :
                        try :
                            os.makedirs( self.cwd + cfg[dir] )
                        except :
                               return False
                   else :
                        return False

          self.cfg = cfg
          
          if ( self.cmd_line.port != None ) :
               self.cfg['server_port'] = int( self.cmd_line.port )
          if ( self.cmd_line.reboot != None ) :
               self.cfg['reboot_time'] = int( self.cmd_line.reboot ) * 60
          else :
               self.cfg['reboot_time'] = int( cfg['reboot_time'] ) * 60
          if ( self.cmd_line.symbols != None ) :
               self.cfg['dbg_symbols_url'] = self.cmd_line.symbols
          else :
               self.cfg['dbg_symbols_url'] = cfg['def_sym'] 

          self.cfg['app_path'] = self.cmd_line.browser
          self.cfg['app_name'] = get_file_name_from_path( cfg['app_path'] )

          self.cfg['tc_url'] += ':' + str( self.cfg['server_port'] ) + '/' + self.cfg['tc_file']

          if ( self.__chck_env( install ) == False ) :   #todo 
               return False

          return True