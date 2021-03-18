#!/bin/bash

date1=`date +%Y%m%d_%H`
minit=`date +%M`
minit2=$(((10#$minit / 5 ) * 5))

if [ $minit2 -lt 10 ]; then
   minit1=0${minit2}
else
   minit1=${minit2}
fi

masani=${date1}${minit1}00

file1=console_run_continously_MACD_anyuser_${masani}.log

echo "PC-TALIBR2+cromox@PC-TALIBR2 /cygdrive/c/Users/cromox/PycharmProjects/Trading212/Forex_CFD/run_nonstop" > "$file1"
echo "$ python3 run_continously_MACD_anyuser.py >" "$file1" "2>&1" >> "$file1"
echo >> "$file1"
echo "PC-TALIBR2+cromox@PC-TALIBR2 /cygdrive/c/Users/cromox/PycharmProjects/Trading212/Forex_CFD/run_nonstop" >> "$file1"
echo "$ cat" "$file1" >> "$file1"
echo >> "$file1"

# /cygdrive/c/tools/Python38/python.exe run_semi_auto_MACD_anyuser.py | tee -a "$file1"
# /cygdrive/c/tools/Python38/python.exe run_semi_auto_MACD_anyuser.py >> "$file1" 2>&1 | tee -a "$file1"
/cygdrive/c/tools/Python38/python.exe run_semi_auto_MACD_anyuser.py 2>&1 | tee -a "$file1"
