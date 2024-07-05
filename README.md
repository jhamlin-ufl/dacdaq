# Diamond Anvil Cell Data AQuistion (DACDAQ)

QT / Python based data  acquisition program.

## About this branch

This branch is for developing the data acquisition system using pyvisa etc.

## Getting GPIB working in Debian Bookworm

Following this:
https://gist.github.com/ochococo/8362414fff28fa593bc8f368ba94d46a

Had to also install linux headers for make to succeed:
sudo apt-get install linux-headers-$(uname -r)

## Problem with location of modules

- From inside my poetry environment I can import pyvisa but not gpib
- From by default system environment I can import gpib but not pyvisa
- the gpib.py module is located in /usr/local/lib/python3.11/dist-packages/gpib-1.0-py3.11-linux-x86_64.egg

## When the kernel updates

You have rebuild and re-install the modules by hand.

- First get the headers for the currently running kernel (uname -r):
sudo aptitude install linux-headers-6.1.0-22-amd64
- cd into linux-gpib-code/linux-gpib-kernel
- make
- make install
