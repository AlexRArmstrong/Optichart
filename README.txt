This is the Read Me file for Optichart.

Optichart is an electronic eye chart program for Optometrists and others who
check eyes.

It is designed to be run on a Raspberry Pi. On the Pi, without a display server
running, it needs to be run as root to access the display. It normally runs as
the sole user application - taking over the display, and user input is limited
to specified buttons on a remote control. Remote control is achieved with a
TSOP 38238 IR sensor wired to the GPIO pins and LIRC. It can be run in a normal
desktop environment, but this is usually impractical in a clinical setting.

==============================
Requires:
==============================
Python 2.7.6
Pygame 1.9.1

Untested with any other versions - if you find some that work, let me know!

==============================
Optional:
==============================
pylirc 0.0.5

==============================
Git Repos:
==============================
There are two primary branches to the git repository.

 master - This is the main development repository. It is set for desktop
		  development - that is, you can run the program on your normal computer
		  desktop.  In particular it contains settings for a screen size of
		  1920x1080.
		  
 rpi    - This repo contains some slight configuration modifications so that it
		  will run on the Raspberry Pi. The chart screen size is set so that
		  it will be full screen.
 
==============================
Structure:
==============================

config.conf - The Optichart configuration file. Make instillation specific
settings here!

main.py - Run this! The main starting point.
Section.py - The base class describing one or more characters and their size.
Line.py - A line consists of one or more sections.
Chart.py - A chart is one or more lines.
Slide.py - A slide is a complete chart that has been rendered for display.
Projector.py - The control logic and final update and display functions.

License.txt - The GNU GPL v. 2
README.txt - This file.
TODO.txt - Bugs and things to fix.

/charts - A sampling of charts, some standard, some not so much.
/fonts - A selection of common fonts.

optichart.e4p - Eric4 IDE project file - helpful for development.

==============================
Implementation Notes:
==============================

With both Python and Pygame installed, you should be able to simply run the
main.py file and execute the program. With a regular keyboard attached, use
the Up/Down arrow keys to scroll a chart, and the Left/Right keys to change
charts. Enter will toggle between isolation of a single line/letter and full
screen - takes 4 presses to go one full cycle. Q quits.

To run this on a Raspberry Pi is slightly more work. I used Arch on the Pi as
most of the other distros I tested were too bloated for my application. I tried
two different approaches to remote control. First I tried a USB receiver and
remote sold by the wonderful folks at www.adafruit.com. My client didn't care
for the remote, however, so I had to find something else.  Described most
simply, I use a TSOP 38238 IR receiver connected to the GPIO
pins - 3.3V Source, Ground, and pin 18 (data). I then run LIRC (www.lirc.org)
and pylirc (www.sourceforge.net/project/pylirc) to interface with the sensor and
remote. This is more complex, as you need to setup LIRC, but the advantage is
that you can use any remote you want. I started with the remote that came with
the TV I was using for testing, but later switched to a RCA universal remote.

Have a lot of fun...
-A
