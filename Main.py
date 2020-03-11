# -*- coding: utf-8 -*-

import os
import sys
import time
import shutil

from IO import *
from Config import *
from UI import *
from App import *
from VSystem import * 
from VEvent import *

def main( ) :

    try :
        if ( VSystem.request_dbg_privileges( ) == False ) :
             raise Exception(" Request debugg privileges fail ! " )

        VSys = VSystem( )

        if ( VSys.cfg_path == None ) :
             print "[!]. Config file not found !"
        elif ( VSys.set_cmdopt( parse_command_line( ) ) == None ) :
               print "[!]. Invalid command line option value !"
        elif ( VSys.chck_evn( parse_config_file( VSys.cfg_path ) ) != True ) :
               print "[!]. Installation fail !"
        else :
             show_banner( VSys.cfg )

             while ( True ) :

                     VSys.clear_events( )

                     # -- Run watchdog --
 
                     if ( VSys.watch_dog.run( VSys.cfg['reboot_time'] ) == False ) :
                          IO.stdout( "[!]. VSys.watch_dog.run() -> False !" )
                          break

                     # -- Run App --
                     if ( VSys.run_app( ) == False ) :
                          IO.stdout( "[!]. VSys.run_app() -> False !" )
                          break
          
                     # -- Run tc server --
                     if ( VSys.start_tc_server( ) == False ) :
                          IO.stdout( "[!]. VSys.start_tc_server() -> False !" )
                          break     

                     # -- Run dbg --

                     if ( VSys.dbg_start( True ) == False ) :
                          IO.stdout( "[!]. VSys.dbg_start() -> False !" )
                          break   #!!!! always restart         

                     if ( Dbg.exception_info != None ) :

                          if ( VSys.log( Dbg.exception_info ) != True ) :
                               IO.stdout( '[!]. IO.open_file( crash_log ) -> False !' )
                               break;

                          IO.stdout( '(*). IO files : ' + Dbg.crsh_signature + ' was sucessfully created in ' + VSys.cwd + VSys.cfg['repos_dir'] + ' ! ' )

                     time.sleep( 2 )

                     VSys.dbg_stop( )
                     VSys.stop_tc_server( )
                     VSys.stop_app( )   

                         

    except Exception as e :

           print "[!]. Global exception : " + str( e )

    finally :
            try :
                VSys.dbg_stop( True )
                VSys.stop_tc_server( True )
                VSys.stop_app( True )
                del VSys
            except Exception as e1 :
                   pass
            return

if ( __name__ == "__main__" ) :

     main( ) 
     os._exit( 0 )
