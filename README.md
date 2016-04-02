# blind-dialer
Allows a visually (and somewhat mentally) impaired user to use a land-line phone, by using a fool-proof input device (game controller), audio feedback and a dial-up modem.

## What's the use case?
My grandma is getting more and more visually impaired and also developing a bit of dementia. We've tried a big-button telephone, we've tried a telephone with separate big-button dialers, we've added a cd-player with somebody talking on it ("to call Jan, press the first button, to call ... etc") but this became harder and harder for her.

## What does it do?
When granny presses a button, a friendly voice tells her to listen to the names that are coming up, and press a button again if she hears the person she wants to call. Then all of her friends and family are listed. She mashes a button again, is asked to confirm, and an old dial-up modem is used to dial the number for her.

## How does it work?
It needs a few fixed audio files for the main program, and a list of
cleverly named audio files that contain the persons she can call. The
files have the phone number to dial in their file name.

It uses the package pyserial to talk to the modem, and pygame for playing
sounds and reading the game controller.

## What should I do to get it working?
### Make a list of contacts
Record your own audio files, with a contact's name per file.

Name the contact list files something like
<sequence_number>_<name_of_contact>_<phone_number_to_dial>.wav
(for example 1_bill_5551234.wav)
and put them in a directory of your choice.

The sequence number is used to sort the contacts, so you'll have this
program list all the contacts in the order you want.
The name is just for yourself.

In the number to dial you can use special characters that your modem
will allow to enhance the dialing, such as "W" for waiting for a second
dial tone or a "," (comma) for waiting for 2 seconds.

### Connect all the hardware
You'll need a modem (and need to know what its serial port is named)
and a game controller. And speakers.

### Install python and some modules
You'll need python 2.7. (I don't know if it works on python 3 as well.)

You'll also the python packages pyserial and pygame.
Install pyserial with pip, eg with
```sudo pip install pyserial``` (Linux)
or
```python -m pip install pyserial``` (Windows)
.
The package pygame does not come via pip.
For Windows, you'll have to download and install
pygame-1.9.2a0.win32-py2.7.msi (Windows) manually.
For some flavours of Linux, you can type ```sudo apt-get install python-pygame```.

### Start the program
To start the program in Windows, use for example:
```python main.py COM1: d:\contacts```
or in Linux:
```./main.py /dev/ttyUSB0 ./contacts```

For all other options enter:
```./main.py --help```

## What hardware do you use?
A raspberry pi, a cheap usb-to-serial converter ("USB 2.0 to Serial RS232 DB9 9-Pin Adapter Cable GPS" on ebay), an old external serial dial-up modem I got from my local craigslist, a simple usb wired gamepad, and some pc speakers.

Maybe you could use a usb dial-up modem, but be certain sure that your operating system has drivers for it.

## Why python?
I'm a Java programmer, but the combination Java, game controllers and raspberry pi gave me... well... nothing. Python on Raspbian had both the pyserial and pygame packages by default.

## Your code is terrible!
No it isn't! I think. It's my first python project. Spare me! Or better: tell me what could be better.
