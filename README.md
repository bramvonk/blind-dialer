# blind-dialer
Allows a visually (and somewhat mentally) impaired user to use a land-line phone, by using a fool-proof input device (game controller), audio feedback and a dial-up modem.

## what's the use case?
My grandma is getting more and more visually impaired and also gaining a bit of dementia. We've tried a big-button telephone, we've tried a telephone with separate big-button dialers, we've added a cd-player with somebody talking on it ("to call Jan, press the first button, to call ... etc") but this became harder and harder for her.

## what does it do?
When granny presses a button, a friendly voice tells her to listen to the names that are coming up, and press a button again if she hears the person she wants to call. Then all of her friends and family are listed. She mashes a button again, is asked to confirm, and an old dial-up modem is used to dial the number for her.

## how does it work?
It needs a few fixed audio files for the main program, and a list of cleverly named audio files that contain the persons she can call. The files have the phone number to dial in their file name.
It uses the package pyserial to talk to the modem (install if needed using pip). I've used the package pygame for communicating with a game controller and playing audio files. I've used pygame-1.9.2a0.win32-py2.7.msi during testing.

## what should I do to get it working?
Record your own audio files, name the contact list files something like <sequence_number>_<name_of_contact>_<phone_number_to_dial>.wav. 
TODO Start program with 2 arguments: 
- name of serial port (eg COM1: in Windows or /dev/ttyUSB0 in linux) 
- the directory that contains the contact list files (I wanted to be able to have those on a separate USB flash drive).

## what hardware do you use?
A raspberry pi, a cheap usb-to-serial converter ("USB 2.0 to Serial RS232 DB9 9-Pin Adapter Cable GPS" on ebay which cost me a dollar and 3 weeks of waiting), an old external serial dial-up modem I got from my local craigslist, a simple usb wired gamepad (also craigslist), and some pc speakers.
Maybe you could use a usb dial-up modem, but be certain sure that your operating system has drivers for it.

## why python?
I'm a Java programmer, but the combination Java, game controllers and raspberry pi gave me... well... nothing. Python on Raspbian had both the pyserial and pygame packages by default.

## your code is terrible!
No it isn't! I think. It's my first python project. Spare me!
