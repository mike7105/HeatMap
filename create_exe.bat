O:\Progs\Python\HeatMap\venv\Scripts\activate
pyinstaller --onefile ^
--noconsole ^
--icon=modules\ico\map_512x512_35976.ico ^
--add-data "modules/ico";"modules/ico" ^
--hidden-import pyreadstat ^
--hidden-import pyreadstat.pyreadstat ^
--hidden-import pyreadstat._readstat_writer ^
--hidden-import pyreadstat.pyreadstat.worker ^
--hidden-import pyreadstat.worker ^
-n HeatMap_v1.9.exe ^
HeatMap.pyw
pause