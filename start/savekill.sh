#!/bin/bash

# Check if EmulationStation is running. Finish the script if doesn't.
espid="$(pgrep -f "/opt/retropie/supplementary/.*/emulationstation([^.]|$)")" || exit 0

# the "sed" command below isn't a crypted message :), it's just a trick to
# make $emucall regex-safe to use in the "pgrep -f" below.
emucall="$(sed '4!d; s/\([\\"]\|[[:alnum:]_]\+=[^ ]* \)//g; s/[][(){}^$*.|+? ]/\\&/g' /dev/shm/runcommand.info)"

# If there's an emulator running, we need to kill it and go back to ES
if [[ -n "$emucall" ]]; then
    emupid="$(pgrep -f "$emucall" | tr '\n' ' ')"
    pkill -P "$(echo $emupid | tr ' ' ',')"
    kill "$emupid"
    wait "$emupid"
    #sleep 5 # maybe it can be lesser
fi

kill "$espid"
wait "$espid"