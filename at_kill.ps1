#AT : powershell -executionpolicy bypass -File F:\Cyklon-MM-2018.05.20\Concepts\PS\at_kill.ps1  "C:\Python27\python.exe" "F:\Cyklon-MM-2018.05.20\Concepts\Clear-22.06.2018\Main.py -browser blablabal.exe"

$LOG_NAME = "at_kill_ps.log"

$victims = @( "windbg", "python", "php", "perl", 
              "MicrosoftEdge", "ApplicationFrameHost", "MicrosoftEdgeCP", 
			  "RuntimeBroker", "browser_broker",
    		  "firefox",
              "chrome"
			);
					
$s_path = split-path $MyInvocation.MyCommand.Definition

$TMP = ""

$RET_MSG = "*****************************`r`n"
$RET_MSG = $RET_MSG + (Get-Date).ToString( ) + "`r`n"

Write-Output $args.count
if ( $args.count -ne 2 ) {
     $TMP = $TMP + "Invalid command line argumments `r`n"
} else {
					
  foreach ($proc in $victims) {
           try {
		        $ErrorActionPreference = "Stop";
                Stop-Process -Force -Name $proc;
	       } catch {
		     $TMP = ( $TMP + $_.Exception.Message + "`r`n" );
		   } finally {
		     $ErrorActionPreference = "Continue";
		   }
  }
  #run 
  $in_arg = $args[1..$args.length]
  Start-Process -FilePath $args[0] -ArgumentList $in_arg
  
}

if( ![string]::IsNullOrEmpty($TMP) )  {
    $RET_MSG = ( $RET_MSG + $TMP )
    $LOG_FILE = ( $s_path + "\" + $LOG_NAME )
	
    Out-File -FilePath $LOG_FILE -Append -InputObject $RET_MSG
}
