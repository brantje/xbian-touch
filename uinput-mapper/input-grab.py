#!/usr/bin/env python
import ctypes, fcntl, os, sys
import select

import uinputmapper
import uinputmapper.linux_uinput
from uinputmapper.cinput import *
from uinputmapper.mapper import KeyMapper, parse_conf, pretty_conf_print

try:
    import cPickle as pickle
except ImportError:
    import pickle

import optparse

_usage = 'input-read /dev/input/event<0> ... /dev/input/event<N>'
parser = optparse.OptionParser(description='Read input devices.',
        usage = _usage,
        version='0.01')
parser.add_option('-D', '--dump', action='store_false',
        default=True, help='Dump will marshall all the events to stdout')
parser.add_option('-v', '--verbose', action='store_true',
        default=False, help='Enable verbose mode (do not combine with -D)')

parser.add_option('-C', '--compat', action='store_true',
        help='Enable compatibility mode; for Python < 2.7')

args, input_file = parser.parse_args()

if len(input_file) == 0:
    parser.print_help()
    exit(0)

# Open input devices
fs = map(InputDevice, input_file)

# Create configuration
config = {}
for idx, f in enumerate(fs):
    c = parse_conf(f, idx)

    config.update(c)

if args.verbose:
    pretty_conf_print(config)

poll_obj, poll_mask = (select.poll, select.POLLIN) if args.compat else \
        (select.epoll, select.EPOLLIN)

# Add all devices to epoll
pp = poll_obj()
for f in fs:
    pp.register(f.get_fd(), poll_mask)

f.grab()

while True:
    pass
