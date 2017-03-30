REM @echo off
REM tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
REM if not "%ERRORLEVEL%"=="0" (
echo Scrape not running-- restarting scrape
netsh interface set interface "Wi-Fi" Disable
TIMEOUT 30
netsh interface set interface "Wi-Fi" Enable
TIMEOUT 100
netsh wlan connect name=belkin.f6a
REM netsh wlan connect name=QuodEratDemonstrandum
REM TIMEOUT 10
REM netsh wlan connect name=belkin.f6a
REM netsh wlan connect name=Pretty Fly For a WiFi
REM netsh wlan connect name=Chelsea's iPhone
REM )
REM if "%ERRORLEVEL%"=="0" (
	REM echo Scrape is still running
	REM TIMEOUT 10
	REM )

REM pause