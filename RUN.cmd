if exist .lock (
   goto __skip__
)

powershell -executionpolicy bypass -File E:\Monitor\at_kill.ps1  
del /Q /S %temp%\* 
rmdir /Q /S %temp%\*
start "C:\Python27\python.exe" "E:\Monitor\Main.py" -browser "C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe"

REM "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/

REM "C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe"

REM "C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe"

REM "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/

:__skip__

REM "C:\Program Files\internet explorer\iexplore.exe"


REM "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -symbols http://msdl.microsoft.com/download/symbols;https://chromium-browser-symsrv.commondatastorage.googleapis.com

REM http://msdl.microsoft.com/download/symbols;https://chromium-browser-symsrv.commondatastorage.googleapis.com
REM "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/

REM "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
REM "C:\Program Files\internet explorer\iexplore.exe"


REM "C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe"

REM "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/