REM For /f "tokens=2-4 delims= " %%a in ('date /t') do (set mydate=%%c.%%a.%%b)
for /f %%x in ('wmic path win32_localtime get /format:list ^| findstr "="') do set %%x
set today=%Month%.%Day%.%Year%

echo %today%


schtasks /create /sc once /ri 5 /tn "YelpScrape"  /st 12:00 /DU 24:00 /tr "D:\Yelp\Yelp_Scrapes\run_scrape_restart %today% 
