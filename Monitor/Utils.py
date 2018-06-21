# encoding=utf8

import os
import re

def chck_port_range( port ) :
    
    Tport = int( port )
	
    if ( ( Tport <= 0 ) or ( Tport > 65535 ) ) :
           return -1
    return Tport
	
def chck_is_url( url ) :
    
    patern = re.compile( r'^(?:http|ftp)s?://'
	                 r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
	                 r'localhost|' 
	                 r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' 
	                 r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' 
	                 r'(?::\d+)?' 
	                 r'(?:/?|[/?]\S+)$', re.IGNORECASE )

    if ( patern.match(url) != None ) :
         return True
    else :
         return False

    
	


def get_file_name_from_path( path ) :

    return os.path.basename( path )