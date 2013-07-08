#!/bin/bash

export LD_LIBRARY_PATH=/usr/local/lib
export TSLIB_CONSOLEDEVICE=none
export TSLIB_FBDEVICE=/dev/fb0
#NOTE: Change '/dev/input/event2', to find event# use 'ls -l /dev/input/by-id'
export TSLIB_TSDEVICE=/dev/input/event2
export TSLIB_CALIBFILE=/etc/pointercal
export TSLIB_CONFFILE=/usr/local/etc/ts.conf
export TSLIB_PLUGINDIR=/usr/local/lib/ts

ts_calibrate