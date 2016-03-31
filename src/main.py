#!/usr/bin/env python
# my source files
import modem
import joystick
import sound
import contacts

# other imports
import time
import argparse


parser = argparse.ArgumentParser(description="Land line dialer with user input from single button presses on a " +
                                             "game controller, and user feedback with audio.")
parser.add_argument("modem_port",
                    metavar="modem-port",
                    help="The name of the serial port to use for the modem, " +
                         "e.g. COM1: for Windows, or /dev/ttyS0 in Linux.")
parser.add_argument("contacts_directory",
                    metavar="contacts-directory",
                    help="The directory that contains the contacts in .wav format, " +
                         "each file having a file name ordernumber_name_phonenumber.wav, " +
                         "for example 1_bill_55523423.wav .")
parser.add_argument("-l", "--locale",
                    dest="locale",
                    help="Indicates the directory in ./sounds to use for the program's audio feedback. " +
                         "Defaults to 'en'.",
                    default="en")
parser.add_argument("-t", "--reaction-time",
                    metavar="REACTION-TIME",
                    dest="reaction_time",
                    help="Number of seconds to wait for button presses after e.g. a contact's name has sounded. " +
                         "Defaults to 3.",
                    type=float,
                    default=3.0)
args = parser.parse_args()
modem_port = args.modem_port
contacts_directory = args.contacts_directory
locale = args.locale
reaction_time = args.reaction_time


joy = joystick.Joystick()
sound_player = sound.SoundPlayer()
contacts = contacts.load_contacts(contacts_directory)

SOUND_DIRECTORY = "sounds/" + locale + "/"
SOUND_PICK_UP_THE_HANDSET = SOUND_DIRECTORY + "pick_up_the_handset.wav"
SOUND_DIALING_FAILED = SOUND_DIRECTORY + "dialing_failed.wav"
SOUND_PRESS_WHEN_YOU_HEAR_THE_RIGHT_PERSON = SOUND_DIRECTORY + "press_when_you_hear_the_right_person.wav"
SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_1 = SOUND_DIRECTORY + "are_you_sure_you_want_to_call_part_1.wav"
SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_2 = SOUND_DIRECTORY + "are_you_sure_you_want_to_call_part_2.wav"
SOUND_DID_NOT_DIAL_BECAUSE_YOU_DID_NOT_CONFIRM = SOUND_DIRECTORY + "did_not_dial_because_you_did_not_confirm.wav"
SOUND_NO_CONTACT_SELECTED = SOUND_DIRECTORY + "no_contact_selected_press_again_to_try_again.wav"


def dial(phone_number):
    try:
        # using "with" automatically cleans up modem,
        # see http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
        with modem.modem(modem_port) as mod:
            # modem ok?
            mod.send_command_and_expect_ok("AT")

            # Enable speaker until a carrier signal is detected
            mod.send_command_and_expect_ok("ATM1")

            # Enable busy detection, disable dialtone detection. Result codes 0-5,7,10 enabled.
            mod.send_command_and_expect_ok("ATX3")

            # Call the number, semicolon says: "Resume command mode after dialing."
            mod.send_command_and_expect_ok("ATDT%s;" % phone_number)

            # tell granny to pick up the receiver...
            sound_player.play_sound_blocking(SOUND_PICK_UP_THE_HANDSET)

            # wait a while
            time.sleep(reaction_time)

            # let the modem hang up. Granny should have the handset now, which will keep the connection open.
            mod.send_command_and_expect_ok("ATH")
    except Exception as exception: # I know this is too broad, but I don't want any error while dialing to stop this program.
        print type(exception).__name__ + ", " + str(exception)
        sound_player.play_sound_blocking(SOUND_DIALING_FAILED)


def play_and_wait_for_button_press(sound_filename, timeout_seconds):
    sound_player.play_sound(sound_filename)

    # wait for joystick presses while the sound plays (we don't want to use a blocking sound player, because
    # I'm too lazy to do joystick presses in a thread or something)
    while not sound_player.is_sound_done_playing():
        if joy.wait_for_button_press(0.1):
            sound_player.stop_playing()
            return True

    # wait for timeout_seoncs seconds before giving up. Return if a joystick button was pressed
    return joy.wait_for_button_press(timeout_seconds)


while True:
    # wait for granny to press a button
    joy.wait_for_button_press()

    # let granny know what to do
    sound_player.play_sound_blocking(SOUND_PRESS_WHEN_YOU_HEAR_THE_RIGHT_PERSON)
    time.sleep(reaction_time)

    # loop through all contacts, play their sounds, and wait for joystick press
    selected_a_contact = False
    for contact in contacts:
        if play_and_wait_for_button_press(contact.sound_filename, reaction_time):
            selected_a_contact = True
            # ask for confirumation
            if play_and_wait_for_button_press(SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_1, 0) or \
                    play_and_wait_for_button_press(contact.sound_filename, 0) or \
                    play_and_wait_for_button_press(SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_2, reaction_time):
                dial(contact.phone_number)
            else:
                sound_player.play_sound_blocking(SOUND_DID_NOT_DIAL_BECAUSE_YOU_DID_NOT_CONFIRM)
            break

    if not selected_a_contact:
        sound_player.play_sound_blocking(SOUND_NO_CONTACT_SELECTED)
