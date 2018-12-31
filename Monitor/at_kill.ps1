#AT : powershell -executionpolicy bypass -File F:\Cyklon-MM-2018.05.20\Concepts\PS\at_kill.ps1  "C:\Python27\python.exe" "F:\Cyklon-MM-2018.05.20\Concepts\Clear-22.06.2018\Main.py -browser blablabal.exe"

$LOG_NAME = "at_kill_ps.log"

$victims = @( "windbg", "python", "php", "perl", 
              "MicrosoftEdge", "ApplicationFrameHost", "MicrosoftEdgeCP", 
			  "RuntimeBroker", "browser_broker","MicrosoftWebDriver",
    		  "firefox","iexplore","IEDriverServer","geckodriver",
              "chrome"
			);
					
$s_path = split-path $MyInvocation.MyCommand.Definition

$TMP = ""

$RET_MSG = "*****************************`r`n"
$RET_MSG = $RET_MSG + (Get-Date).ToString( ) + "`r`n"

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

$RET_MSG = ( $RET_MSG + $TMP )
$LOG_FILE = ( $s_path + "\" + $LOG_NAME )
	
Out-File -FilePath $LOG_FILE -Append -InputObject $RET_MSG;


