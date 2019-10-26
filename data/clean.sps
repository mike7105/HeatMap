* Encoding: windows-1251.
-include file= 'm:\Macros0\m13-0\app.sps'.
-include file= 'm:\Macros0\m13-0\xCollection.sps'.

CD "O:\Progs\Python\HeatMap\data".

get file="Fanta_Pear.sav"/keep id  Conc_1_B4_1_x to Conc_2_B4_30_y Conc_1_B5_1_x to Conc_2_B5_30_y Conc_1_B6_1_x to Conc_2_B6_30_y Conc_1_B7_1_x to Conc_2_B7_30_y.
sort cases by id.

/*******сначала нажо вытянуть файл по концепции.
SPSSINC SELECT VARIABLES  MACRONAME="!CONC1" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1.*" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!CONC2" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_2.*" /OPTIONS ORDER=FILE PRINT=yes.

save outfile="temp1.sav".


MKCELL
 file={temp1.sav}
 outfile={temp2.sav}
 keep={id}
 var={conc}
 list={
1 !CONC1
2 !CONC2
}.
exe.


/******вытянуть файл по координатам.
SPSSINC SELECT VARIABLES  MACRONAME="!B4_x" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B4.*x" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!B4_y" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B4.*y" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!B5_x" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B5.*x" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!B5_y" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B5.*y" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!B6_x" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B6.*x" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!B6_y" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B6.*y" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!B7_x" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B7.*x" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!B7_y" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN="^Conc_1_B7.*y" /OPTIONS ORDER=FILE PRINT=yes.

VARSTOCASES
/MAKE B4_x FROM !B4_x
/MAKE B4_y FROM !B4_y
/MAKE B5_x FROM !B5_x
/MAKE B5_y FROM !B5_y
/MAKE B6_x FROM !B6_x
/MAKE B6_y FROM !B6_y
/MAKE B7_x FROM !B7_x
/MAKE B7_y FROM !B7_y
/INDEX = ind
/KEEP = id conc
/NULL = KEEP.
exe.


/*comp unique=id*1000+conc*100+ind.
/*exe.

/******вытянуть файл по вопросам.
SPSSINC SELECT VARIABLES  MACRONAME="!X" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN=".*x" /OPTIONS ORDER=FILE PRINT=yes.
SPSSINC SELECT VARIABLES  MACRONAME="!Y" VARIABLES=ALL /PROPERTIES TYPE=NUMERIC   PATTERN=".*y" /OPTIONS ORDER=FILE PRINT=yes.

VARSTOCASES
/MAKE X FROM !X
/MAKE Y FROM !Y
/INDEX = qst
/KEEP = id conc ind
/NULL = KEEP.
exe.

val lab conc 1 "Conc1.JPG" 2 "Conc2.JPG".
val lab qst 1 "B4" 2 "B5" 3 "B6" 4 "B7".

 * String Pict (A9).
 * comp Pict = concat("Conc", string(conc,F1), ".JPG").
 * fre Pict.
recode X Y (sysm=-1).
save outfile="Coords.sav".

get file="Coords.sav".
save translate outfile="coords.csv" /type=csv /cells=labels /fieldnames /replace.

get file="Coords.sav".

comp part=1.
add files
/file=*
/file="Coords.sav".
exe.

recode part (sysm=2).

if part=2 conc=conc+2.
add val lab conc 3 "Conc3.JPG" 4 "Conc4.JPG".

fre conc.

save translate outfile="coords2.csv" /type=csv /cells=labels /fieldnames /replace.

recode X Y (-1=sysm).

save outfile="Coords2.sav".