uinput-mapper
=============

uinput-mapper maps input devices to new virtual input devices, using (as implied
by the name /dev/uinput[1]).

[1] Or /dev/input/uinput depending on the OS.


Usage and Configuration
=======================

Configuration is done in Python; examples and other information can be found on
the project website: http://hetgrotebos.org/wiki/uinput-mapper

Bugs
====

None that I am aware of, but if you find some please drop me a mail at
http://wizzup.org. (You can find my email address there)


linux_input.py
==============

Python binding for linux/input.h ; somewhat incomplete.
Included in uinput-mapper ; may be split later

linux_uinput.py
==============


Python binding for linux/uinput.h ; not complete yet.
Included in uinput-mapper ; may be split later


Development notes
=================

Generating gen.py:

    gcc -E -dM /usr/include/linux/input.h | egrep ' (EV|SYN|KEY|BTN|REL|ABS|MSC|LED|SND|REP|SW)_[A-Za-z0-9_]+' | ( echo "#include <linux/input.h>" ; echo "input_constants_dict = {" ; sed -r 's/[^ ]+ +([^ ]+).*/"\1" : \1,/' ; echo "}" ) | gcc -E -o /dev/stdout - | grep 'input_constants_dict = {' -A 100000 > gen.py
