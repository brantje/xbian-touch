#!/bin/bash

TS_EV=`ls -l /dev/input/by-id | grep "eGalax"`
export TS_EV=${TS_EV#*/}
export UIMAPPER_DEV="/dev/input/$TS_EV"
echo $TS_EV
echo $UIMAPPER_DEV
