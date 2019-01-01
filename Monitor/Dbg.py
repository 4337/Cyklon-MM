# -*- coding: utf-8 -*-

import os
import time
import winappdbg
import threading
import psutil
import shutil
import hashlib
import datetime

from IO import *
from VEvent import *
from Utils import *
from winappdbg import *
from time import localtime, strftime

class DbgEventHandler( EventHandler ) :

      crash_course = [ '0xc0000005L', #access violation 
                       '0xc0000409L', #
                       '0x80000001L', #
                       '0xC0000096L', #
                       '0xC000001DL' #, # 
                       #'0xc00000fdL'  #stack overflow
                     ]

      def __init__( self, cwd ) :

          self.exploitable_log_file = cwd + "exploitable.log.txt"
          super( DbgEventHandler, self ).__init__( )

      '''
      /***************************************************************************************************
       *  format output and all other stuff 
       ***************************************************************************************************/
      '''
      def __signature( self, sig_obj ) :
     
          part = sig_obj.split(' ')
          md = hashlib.md5( )
          part[3] = part[3].replace( '+', '_' )
          part[3] = part[3].replace( '::', '@' )
          part[3] = part[3].replace( '<', '[' )
          part[3] = part[3].replace( '>', ']' )
          md.update( part[0] + str(part[1]) + part[3] )
          out = md.hexdigest( ).upper( ) + '_' + part[3]
          return out

      '''
      ######## end format output and ... ########################################################################## 
      '''
 
      '''
      /***************************************************************************************************
       * start events 
       ***************************************************************************************************/
      '''
      def event(self, event) :

          pass
 
      def create_process(self, event) :  #TODO: attach 2 new proc if is not debuggee
  
          winappdbg.Color.yellow( )
          IO.stdout( '(*). Dbg create_process event (pid : ' + str( event.get_pid() ) + ') !' )
          winappdbg.Color.default( )
          

      def exit_process( self, event ) : 

          try :
              pid = event.get_pid( ) 
              proc = event.get_process( )

              winappdbg.Color.blue( )
              IO.stdout( '(*). Dbg processes [' + str( Dbg.dbg.get_debugee_count( ) ) + '] | Process ID ' + str( pid ) + ' | died ' )
              winappdbg.Color.default( )

              for index in enumerate( Dbg.targets ) :
                  if ( pid == Dbg.targets[index].get_pid( ) ) :
                       Dbg.targets.pop(index)

              #if ( Dbg.dbg.get_debugee_count( ) == 0 ) :
              VEvent.reboot.set( )
          except :
                 pass

      def rip( self, event  ):  

          winappdbg.Color.bk_yellow( )
          IO.stdout( '(x). Dbg debugger error ' + event.get_exception_name() + ' !' )
          winappdbg.Color.bk_default( ) 
          VEvent.reboot.set( ) 

      def exception( self, event ) :

          exc_code = hex( event.get_exception_code( ) )

          if ( ( str(exc_code) in DbgEventHandler.crash_course ) and ( event.is_first_chance( ) == True ) ) :  

               VEvent.no_freeze.clear( )

               get_sym = True

               Proc = event.get_process( )
               syms = os.listdir( Dbg.sym_dir )
           
               if ( len( syms ) >  0 ) :
                    diff = datetime.datetime.now() -  datetime.datetime.utcfromtimestamp( os.stat( Dbg.sym_dir + '\\' + syms[0]  ).st_ctime ) 
                    IO.stdout( 'Syms test diff.s = '+str(diff.seconds / 60) + ' sym.r = ' + str(Dbg.sym_reload) ) #test
                    if ( ( int(diff.seconds) / 60 ) <= int(Dbg.sym_reload / 60)  ) :  #TODO: chck ! 
                           get_sym = False
                    else :
                         shutil.rmtree( Dbg.sym_dir ) #clear symbols
                  
               if ( get_sym == True ) :  

                    winappdbg.Color.magenta( )             
                    IO.stdout( '     Exception occured | download symbols ! |' )
                    winappdbg.Color.default( )
                    try :
                        if ( len( Proc.get_symbols( ) ) <= 0 ) :  #FIX !!!!!!!!!!!!!!!!!!!!
                             IO.stdout( '(*). Dbg symbols loading error !' )
                    except Exception as e :
                                          print IO.stdout( '(!). Dbg symbols loading exception : ' + str(e) + ' !' )

               Crsh = winappdbg.Crash( event )

               Dbg.exception_info = IO.stdout( "     Exception (" + str( event.get_pid( ) ) + ") : " )
               winappdbg.Color.red( )
               IO.stdout("     " + Crsh.exceptionName + ' at : ' + Crsh.exceptionLabel + ' [ ' + str(hex(Crsh.exceptionAddress)) + ']' )
               winappdbg.Color.default( )
 
               Dbg.crsh_signature = self.__signature( Crsh.signature[0] + " " + str(Crsh.signature[1]) + " " + str(Crsh.signature[2]) + " " + str(Crsh.signature[3]) )
               IO.stdout( "     Signature : " )
               winappdbg.Color.blue( )
               IO.stdout( "     " + Dbg.crsh_signature  )
               winappdbg.Color.default( )

               IO.stdout( "     Exploitable : " )
               Explo = Crsh.isExploitable( )
   
               if ( ( Explo[0] == 'Probably exploitable' ) or ( Explo[0] == 'Exploitable' ) ) :
                      if ( IO.open_file( self.exploitable_log_file, 'a' ) != False ) :
                           IO.write_file(  Dbg.crsh_signature + "\r\n" )
                           IO.close_file( )
                      else :
                           IO.stdout( '(*). IO create log file (Exploitable) failed  !' )
  
               winappdbg.Color.green( )
               IO.stdout( "     desc : " + Explo[1] + " : " + Explo[0] ) 
               winappdbg.Color.default( )
                   
               Crsh.fetch_extra_data( event, takeMemorySnapshot = 0 )
               Dbg.exception_info = Crsh.fullReport( )

               winappdbg.Color.light( )
               IO.stdout( '--------------------------------------------------------------' )
               winappdbg.Color.bk_magenta( )
               IO.stdout( Dbg.exception_info )
               winappdbg.Color.bk_default( )
               IO.stdout( '--------------------------------------------------------------' )
               winappdbg.Color.default( )

               VEvent.no_freeze.set( )
          
          if ( event.is_noncontinuable( ) == True ) :  #wyjatek nie kontynowalny - reboot

               VEvent.reboot.set( )
 

class Dbg :
  
      dbg = None
      targets = []
      symbols_path = ''
      exception_info = None
      crsh_signature = None
      sym_dir = ''
      sym_reload = 30  
      
      @staticmethod
      def set_symbol_reload( timeo ) :
          
          t = int( timeo ) 
          if ( t > 0 ) :
               Dbg.sym_reload = t

      @staticmethod
      def set_symbol_path( sym_urls, sym_dir ) :

          sym_urls = sym_urls.split( ';' )

          for url in sym_urls :
              Dbg.symbols_path += 'cache*' + str(sym_dir) + ';srv*' + str(url) + ';' 

          IO.stdout( '(*). Dbg symbols : ' + Dbg.symbols_path )

          return winappdbg.System.fix_symbol_store_path( symbol_store_path = Dbg.symbols_path, force = True )
 

      def __init__( self, sym_dir, anty_dbg = True, reboot_on_error = False, dbg_help = '' ) :
 
          Dbg.sym_dir = sym_dir
          self.cwd = os.path.dirname( os.path.realpath( __file__ ) ) + "\\"
          self.reboot_on_error = reboot_on_error
          self.dbg_event = DbgEventHandler( self.cwd )
          Dbg.dbg = Debug( self.dbg_event, bHostileCode = anty_dbg )

          if ( dbg_help != '' ) :
               if ( os.path.isfile( dbg_help ) == True ) :
                    Dbg.dbg.system.load_dbghelp( dbg_help  ) 
               else :
                    IO.stdout( '(!). Dbg dbghelp.dll not exisit ' + str(dbg_help) + ' !' )

      def __del__( self ) :

          if ( Dbg.dbg.get_debugee_count( ) > 0 ) :
               for trg in Dbg.targets :
                   if ( trg != None ) :
                        pid = trg.get_pid( )
                        if ( psutil.pid_exists( pid ) == True ) :
                             try : 
                                 Dbg.dbg.detach( pid )
                             finally :
                                     try :
                                          psutil.Process( pid ).kill( )
                                          winappdbg.Color.light( )
                                          IO.stdout( '(*). Dbg kill process with ID (' + str( pid ) + ') : done !' )
                                          winappdbg.Color.default( )
                                     except Exception as e :
                                            #print 'Exception in Dbg.__del__() ' + str(e)
                                            pass
                                 
          
          Dbg.sym_dir = ''
          Dbg.symbols_path = ''
          Dbg.exception_info = None
          Dbg.crsh_signature = None
          del Dbg.targets[:]
          del Dbg.dbg
          del self.cwd

      def stop( self ) :
       
          if ( VEvent.reboot.is_set( ) == False ) :
               VEvent.reboot.set( )
          
      def attach_multi( self, pids ) :
          
          ret = True

          for pid in pids :
              try :
                  if ( psutil.pid_exists( pid ) == True ):
                       proc = Dbg.dbg.attach( pid )
                       IO.stdout( '(*). Dbg attach to ' + proc.get_filename( ) + ' | PID ' + str( pid ) + ' | done !' )
                       dir, file_name = os.path.split( proc.get_filename( ) )
                       g_flag = get_proces_gflag( file_name )
                       if ( g_flag != None ) :
                            winappdbg.Color.bk_green( ) 
                            IO.stdout( '(*). Dbg - process (pid: ' + str(pid) + ') GFlag value : ' + str(g_flag) )
                            winappdbg.Color.bk_default( )
                       else :
                            winappdbg.Color.bk_red( ) 
                            IO.stdout( '(*). Dbg - process (pid: ' + str(pid) + ') GFlag value : undefined' )
                            winappdbg.Color.bk_default( )
                       try :
                           proc.resume( )
                       except Exception as e:  #what now
                              pass
                       Dbg.targets.append( proc )
              except Exception as e:
                     IO.stdout( '(*). Dbg attach 2 process error (' + str( pid ) + ') ' + str( e ) + ' !' )
                     if ( self.reboot_on_error == True ) :
                          ret = False
                          VEvent.reboot.set( )
                          pass
                    # return False #TODO: FIX return i reboot tu niedziala, poza tym return z main jest zepsuty tez cza naprawic

          return ret
         
      def run( self ) :

          break_out = False
          IO.stdout( '(*). Dbg run (' + str( self.dbg.get_debugee_count( ) ) + ') : done !' )
          VEvent.dbg_ready.set( )
          while ( (Dbg.dbg.get_debugee_count( ) > 0) and (break_out != True) ) :

                while ( True ) :
                        if ( VEvent.reboot.is_set( ) == True ) :
                             break_out = True
                             break
                        try : 
                            Dbg.dbg.wait( 100 )   #jezeli jest w watku to rzuca wyjatek
                            break;
                        except WindowsError as e : 
                               if ( e.winerror not in (win32.ERROR_SEM_TIMEOUT, win32.WAIT_TIMEOUT) ) :
                                    raise 
                        except Exception as e :
                               self.reboot.set( ) #end
                try :
                    Dbg.dbg.dispatch( )
                finally :
                        Dbg.dbg.cont( )
           
          # ## 