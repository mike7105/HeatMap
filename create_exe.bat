pyinstaller --onefile ^
--noconsole ^
--icon=modules\ico\map_512x512_35976.ico ^
--add-data "modules/ico";"modules/ico" ^
--hidden-import pyreadstat ^
--hidden-import pyreadstat.pyreadstat ^
--hidden-import pyreadstat._readstat_writer ^
HeatMap.pyw
pause