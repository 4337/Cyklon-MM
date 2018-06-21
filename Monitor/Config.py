# encoding=utf8

from ConfigParser import SafeConfigParser

class ConfigException( Exception ) :
      
	  def __init__( self, value ) :
	      self.value = value
	  def __str__( self ) :
	      return repr( self.value ) 

def parse_config_file( cfg_path ) :

    RetVal = { }
    RetVal['gdbhelp'] = ''
    Parser = SafeConfigParser( )
	
    if ( len( Parser.read( cfg_path ) ) > 0) : 
            try :           
                RetVal['gdbhelp'] = Parser.get( 'Debugger', 'dgbhelp' ) #(optional) full path 2 gdbhelp.dll
            except :
                   pass
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