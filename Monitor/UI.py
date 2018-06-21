# encoding=utf8

import os
import argparse
from Utils import *
  
def chck_arg_port_range( port ) : 

    Tport = chck_port_range( port )
	
    if ( Tport == -1 ) :
	
	    raise argparse.ArgumentTypeError( 'invalid range : use port from range (1 - 65535)' )
	
    return Tport

def chck_arg_is_url( url ) :
     
	IsUrl = chck_is_url( url )
	
	if ( IsUrl != True ) :
	
	     raise argparse.ArgumentTypeError( 'invalid value : use [server url] ' )
		 
	return url
	
def parse_command_line( ) : 
    
    CmdLineParser = argparse.ArgumentParser( description = 'Use RunDbg.py -browser X:\path\2\browser.exe -arch x86|x64' )
	
    RequiredArgs = CmdLineParser.add_argument_group('required arguments')
    RequiredArgs.add_argument( '-browser', help = 'Use -browser [path to web browser', type = str, required = True )
	
    CmdLineParser.add_argument( '-symbols', help = '(Optional) Use -symbols URIToDbgSymbolServer', type = chck_arg_is_url )
    CmdLineParser.add_argument( '-reboot', help = '(Optional) Use -reboot (minutes) for reboot after N minutes', type = int )
    CmdLineParser.add_argument( '-port', help = '(Optional) Use -port (1-65535) for testcase server port', type = chck_arg_port_range ) 
	
    Args = CmdLineParser.parse_args()	
	
    if ( ( os.path.isfile( Args.browser ) != True ) ) :
    
       return None
	   
    return Args

def show_banner( opts ) :

    print ( 
            ".--.        .-.   .-.                     .-..-..-..-.\r\n"
            ": .--'      : :.-.: :                     : `' :: `' :\r\n"
            ": :   .-..-.: `'.': :   .--. ,-.,-. _____ : .. :: .. :\r\n"
            ": :__ : :; :: . `.: :_ ' .; :: ,. ::_____:: :; :: :; :\r\n"
            "`.__.'`._. ;:_;:_;`.__;`.__.':_;:_;       :_;:_;:_;:_;\r\n"
            "       .-. :                                          \r\n"
            "       `._.'                                          \r\n"
            "[+]. TC server port : " + str(opts['server_port']) +"\r\n"
	    "[+]. TC server dir  : /" + opts['server_dir'] + "/\r\n"
            "[+]. Symbols uri : " + str(opts['dbg_symbols_url']) + "\r\n"
            "[+]. Repro dir : /" + opts['repos_dir'] + "/\r\n"
            "[+]. Application : " + opts['app_path'] + "\r\n"
            "[+]. TC url : " + opts['tc_url'] + "\r\n" )
