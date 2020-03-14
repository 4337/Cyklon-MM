# -*- coding: utf-8 -*-

from ConfigParser import SafeConfigParser

class ConfigException( Exception ) :
      
	  def __init__( self, value ) :
	      self.value = value
	  def __str__( self ) :
	      return repr( self.value ) 

def parse_config_file( cfg_path ) :

    RetVal = { }
    RetVal['dbghelp'] = ''
    RetVal['tc_tec'] = ''
    RetVal['jit_dbg'] = "0"
    RetVal['jit_dbg_procs'] = None
    
    Parser = SafeConfigParser( )
	
    if ( len( Parser.read( cfg_path ) ) > 0) : 
            try :           
                RetVal['dbghelp'] = Parser.get( 'Debugger', 'dbghelp' ) #(optional) full path 2 dbghelp.dll
            except :
                   pass
            try :
                RetVal['tc_tec'] = Parser.get( 'Fuzzer', 'tec' )
            except :
                   pass
            try :
                RetVal['jit_dbg'] = Parser.get( 'JIT_Debugger','jit_dbg' )
                if (  RetVal['jit_dbg'] != None ) :
                	  if ( int(RetVal['jit_dbg']) != 0 ) :
                           RetVal['jit_dbg_procs'] = Parser.get('JIT_Debugger', 'jit_dbg_procs' )
            except :
            	   pass
            finally :
                    if ( RetVal['jit_dbg_procs'] == None ) :
                         RetVal['jit_dbg'] = "0"

	    try : 
		      
	        RetVal['reboot_time'] = Parser.get( 'Time', 'reboot' )
	        RetVal['server_port'] = Parser.get( 'Server', 'port' )
	        RetVal['symbols_dir'] = Parser.get( 'Debugger', 'symbols_dir' )
	        RetVal['server_dir'] = Parser.get( 'Server', 'dir' )
                RetVal['tc_url'] = Parser.get( 'Server', 'url' )
	        RetVal['tc_generator'] = Parser.get( 'Fuzzer', 'generator' )
	        RetVal['repos_dir'] = Parser.get( 'Logs', 'dir' )
	        RetVal['tc_command'] = Parser.get( 'Fuzzer', 'command' )
                RetVal['drivers_dir'] = Parser.get( 'Selenium', 'drivers_dir' )
                RetVal['tc_file'] = Parser.get( 'Server', 'file' )
                RetVal['def_sym'] = Parser.get( 'Debugger', 'def_sym' )
			  
	    except : 
		     raise ConfigException( 'Invalid config file' )
			 
    return RetVal