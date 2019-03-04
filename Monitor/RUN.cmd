powershell -executionpolicy bypass -File C:\Users\echo\Desktop\Cyklon-31.08.2018\at_kill.ps1 
del /Q %temp%\\* 
start "C:\Python27amd64\python.exe" "C:\Users\echo\Desktop\Cyklon-31.08.2018\Main.py" -browser "C:\Windows\SystemApps\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\MicrosoftEdge.exe"

REM "C:\Program Files\Mozilla Firefox\firefox.exe" -port 80 -symbols http://msdl.microsoft.com/download/symbols;https://symbols.mozilla.org/