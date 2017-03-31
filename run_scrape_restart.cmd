REM runas /savecred /noprofile /user:Administrator C:\Users\cjcrain\Desktop\reset_hotspot_SC.lnk

START D:\Yelp\Yelp_Scrapes\reset_hotspot_sc

REM "C:\Users\cjcrain\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\System Tools\Command Prompt"
REM D:\Yelp\Scrape8_0217\reset_hotspot.bat

TIMEOUT 160
"C:\Program Files\Anaconda2\Scripts\ipython.exe" D:\Yelp\Yelp_Scrape\yelp_scrape9.py %1


REM "C:\Users\Chelsea\Anaconda2\Scripts\ipython.exe" E:\Yelp\Yelp_Scrapes\Scrape9_0317\scrape9.py %*
REM pause
