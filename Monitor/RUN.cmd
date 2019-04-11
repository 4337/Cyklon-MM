powershell -executionpolicy bypass -File C:\Users\echo\Desktop\Cyklon-31.08.2018\at_kill.ps1 
del /Q /S %temp%\* 
rmdir /Q /S %temp%\*
start "C:\Python27amd64\python.exe" "C:\Users\echo\Desktop\Cyklon-31.08.2018\Main.py" -browser "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/

REM "C:\Program Files\internet explorer\iexplore.exe"


REM "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" -symbols http://msdl.microsoft.com/download/symbols;https://chromium-browser-symsrv.commondatastorage.googleapis.com

REM http://msdl.microsoft.com/download/symbols;https://chromium-browser-symsrv.commondatastorage.googleapis.com
REM "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/

REM "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
REM "C:\Program Files\internet explorer\iexplore.exe"


REM "C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe"

REM "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/