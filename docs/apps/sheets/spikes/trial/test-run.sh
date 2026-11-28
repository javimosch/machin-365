S=$1; F=$2; cd $S/trial; rm -f out.xlsx /dev/shm/m365-dump.txt; Xvfb :95 -screen 0 1280x760x24 >/dev/null 2>&1 & X=$!; timeout 2 tail -f /dev/null
DISPLAY=:95 MFL_ARENA_WARN_MB=0 IN=$F OUT=$S/trial/out.xlsx DUMP=/dev/shm/m365-dump.txt ./${BIN:-sheets-trial-v2} >app.log 2>&1 & A=$!; timeout 4 tail -f /dev/null
DISPLAY=:95 timeout 400 /usr/bin/python3 -I ${3:-functional.py} $F $S/trial/out.xlsx /dev/shm/m365-dump.txt $A
kill -0 $A 2>/dev/null && echo "app still running at the end" || { wait $A; echo "APP EXITED $?"; }
DISPLAY=:95 import -window root last.png; kill $A $X 2>/dev/null; wait 2>/dev/null
