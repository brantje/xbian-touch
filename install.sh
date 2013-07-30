#!/bin/bash
echo "XBian touch installer by brantje"
if [ ! -f /etc/pointercal ]; then
	echo  "Listing event devices"
	ls -l /dev/input/by-id | grep event
	echo "What is the event number of the touchscreen? eg: event0 then you type 0, followed by [ENTER]"
	read inputnumber
	sudo stop xbmc
	echo "Getting tslib"
	wget --no-check -O tslib_1-1_armhf.deb "https://github.com/brantje/xbian-touch/raw/master/tslib_1-1_armhf.deb"
	echo "Installing tslib"
	dpkg -i tslib_1-1_armhf.deb
	export LD_LIBRARY_PATH=/usr/local/lib
	export TSLIB_CONSOLEDEVICE=none
	export TSLIB_FBDEVICE=/dev/fb0
	export TSLIB_TSDEVICE=/dev/input/event$inputnumber
	export TSLIB_CALIBFILE=/etc/pointercal
	export TSLIB_CONFFILE=/usr/local/etc/ts.conf
	export TSLIB_PLUGINDIR=/usr/local/lib/ts
	echo "Please follow the instructions on the display..."
	ts_calibrate
	echo "Getting uimapper..."
	wget --no-check -O uimapper.tar.gz "https://github.com/brantje/xbian-touch/raw/master/uimapper.tar.gz"
	echo "Installing uimapper..."
	sudo mkdir -p /scripts && sudo tar -zxf uimapper.tar.gz  -C /scripts

	echo "Generating config file"
	echo "#!upstart
	description \"uimapper\"


	env UIMAPPER_DEV=\"/dev/input/event$inputnumber\"
	env UIMAPPER_CONF=\"configs/touchscreen.py\"
	env UIMAPPER_DIR=\"/scripts/uinput-mapper\"

	start on (input-device-added SUBSYSTEM=input)

	stop on input-device-removed

	nice -10

	kill timeout 1

	expect fork

	script
		chdir \$UIMAPPER_DIR
		exec ./input-read.py \$UIMAPPER_DEV -D | ./input-create.py \$UIMAPPER_CONF &
	end script
	respawn" >> uimapper.conf
	echo "Moving config..."
	sudo mv uimapper.conf /etc/init
	sudo chmod +x /scripts/uinput-mapper/input-create.py
	sudo chmod +x /scripts/uinput-mapper/input-read.py

	echo "Cleaning up..."
	rm uimapper.tar.gz
	rm tslib_1-1_armhf.deb > /dev/null #Silent error
	sudo start uimapper
	sudo start xbmc
	echo "Installation done!"
else
	echo "Already installed... Recalibrating"
	echo  "Listing event devices"
	ls -l /dev/input/by-id | grep event
	echo "What is the event number of the touchscreen? eg: event0 then you type 0, followed by [ENTER]"
	read inputnumber
	sudo stop xbmc
	sudo stop uimapper
	export LD_LIBRARY_PATH=/usr/local/lib
	export TSLIB_CONSOLEDEVICE=none
	export TSLIB_FBDEVICE=/dev/fb0
	export TSLIB_TSDEVICE=/dev/input/event$inputnumber
	export TSLIB_CALIBFILE=/etc/pointercal
	export TSLIB_CONFFILE=/usr/local/etc/ts.conf
	export TSLIB_PLUGINDIR=/usr/local/lib/ts
	sleep 3
	echo "Please follow the instructions on the display..."
	ts_calibrate
	sudo start uimapper
	sudo start xbmc
fi
