#!/usr/bin/env python
import ctypes, fcntl, os, sys

import uinputmapper
import uinputmapper.linux_uinput
from uinputmapper.cinput import *
from uinputmapper.mapper import KeyMapper, parse_conf, pretty_conf_print, \
    get_exported_device_count
from uinputmapper.linux_input import timeval, input_event

try:
    import cPickle as pickle
except ImportError:
    import pickle

import imp
import optparse

_usage = 'python create.py /path/to/config1 ... /path/to/configN'
parser = optparse.OptionParser(description='Create input devices.',
        usage=_usage,
        version='0.01'
        )
parser.add_option('-C', '--compat', action='store_true',
        help='Enable compatibility mode; for Python < 2.7')
parser.add_option('-v', '--verbose', action='store_true',
        help='Enable verbose mode')

args, cfg = parser.parse_args()

# Unpickle from stdin ; currently this is the default and only way
in_f = pickle.Unpickler(sys.stdin)

# Read input device count
nifd = in_f.load()

# Read configuration
conf = in_f.load()

if args.verbose:
    pretty_conf_print(conf)

# Allow configurations to change our current configuration
for path in cfg:
    config_merge = imp.load_source('', path).config_merge
    config_merge(conf)

if args.verbose:
    pretty_conf_print(conf)

m = KeyMapper(conf)

# Get number of output devices (determined from conf)
nofd = get_exported_device_count(conf)

# Create and expose uinput devices
ofs = []
for f in xrange(nofd):
    d = UInputDevice()
    m.expose(d, f)
    d.setup('uimapper - touchscreen')
    ofs.append(d)
 
# Map events

xpos = 0
pxpos = 0
ypos = 0
pypos = 0
xtouch = False
ytouch = False
intouch = False
ptime = 0

while True:
    if not args.compat:
        fd, ev = in_f.load()
    else:
        fd, ev_p = in_f.load()
        ti = timeval(ev_p[0], ev_p[1])
        ev = input_event(ti, ev_p[2], ev_p[3], ev_p[4])
    
    idx, ev = m.map_event(ev, fd)
    d = ofs[idx]
    
    d.fire_event(ev)

# Markamc : Touchscreen BTN_TOUCH time & range test

    if ev.type == EV_ABS and ev.code == ABS_X:
        xpos = ev.value
        if intouch == True and xtouch == False:
            pxpos = xpos
            xtouch = True
    if ev.type == EV_ABS and ev.code == ABS_Y:
        ypos = ev.value
        if intouch == True and ytouch == False:
            pypos = ypos
            ytouch = True

#BTN_TOUCH press event

    if ev.code == BTN_TOUCH and ev.value == 1:
        pev = ev
        intouch = True
        ptime = float(pev.time.tv_sec) + float(pev.time.tv_usec / 1000000.0)
        
#BTN_TOUCH release event

    if ev.code == BTN_TOUCH and ev.value == 0:
        rev = ev
        dx = xpos - pxpos
        dy = ypos - pypos
        intouch = False
	xtouch = False
        ytouch = False
        inrange = (dx * dx) + (dy * dy)
        rtime = float(rev.time.tv_sec) + float(rev.time.tv_usec / 1000000.0)
        holdtime = rtime - ptime

#Range and time check

        if inrange <= 400:
            if holdtime > 0.20 and holdtime <= 0.50:
                rev.code = BTN_TOUCH
                rev.value = 1
                d.fire_event(rev)
                rev.value = 0
                d.fire_event(rev)
                holdtime = 0
            if holdtime > 0.50 and holdtime <= 1.50:
                rev.code = BTN_RIGHT
                rev.value = 1
                d.fire_event(rev)
                rev.value = 0
                d.fire_event(rev)
                holdtime = 0
            if holdtime > 1.5:
                holdtime = 0
