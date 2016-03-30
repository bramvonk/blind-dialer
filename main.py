# my source files
import modem
import joystick
import sound
import contacts

# other imports
import pygame
import time
import sys

if sys.platform == "win32":
    # workaround in windows: windows won't play sounds if pygame.init() has been called (which we need for joystick to
    # work), but you can work around this bug by opening a window...
    # see http://stackoverflow.com/questions/2936914/pygame-sounds-dont-play
    pygame.init()
    screen = pygame.display.set_mode((40, 40), 0, 32)

joy = joystick.Joystick()
sound_player = sound.SoundPlayer()
contacts = contacts.load_contacts("contacts")

SOUND_PICK_UP_THE_HANDSET = "pick_up_the_handset.wav"
SOUND_SORRY_DIALING_FAILED = "sorry_calling_failed.wav"
SOUND_PRESS_WHEN_YOU_HEAR_THE_RIGHT_PERSON = "press_when_you_hear_the_right_person.wav"
SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_1 = "are_you_sure_you_want_to_call_part_1.wav"
SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_2 = "are_you_sure_you_want_to_call_part_2.wav"
SOUND_DID_NOT_DIAL_BECAUSE_YOU_DID_NOT_CONFIRM = "did_not_dial_because_you_did_not_confirm.wav"
SOUND_NO_CONTACT_SELECTED = "no_contact_selected_press_again_to_try_again.wav"


def dial(phone_number):
    try:
        # using "with" automatically cleans up modem,
        # see http://stackoverflow.com/questions/865115/how-do-i-correctly-clean-up-a-python-object
        with modem.modem("COM2:") as mod:
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
            time.sleep(2)

            # let the modem hang up. Granny should have the handset now, which will keep the connection open.
            mod.send_command_and_expect_ok("ATH")
    except: # I know this is too broad, but I don't want any error while dialing to stop this program.
        sound_player.play_sound_blocking(SOUND_SORRY_DIALING_FAILED)


def play_and_wait_for_button_press(sound_filename, timeout_seconds):
    sound_player.play_sound(sound_filename)

    # wait for joystick presses while the sound plays (we don't want to use a blocking sound player, because
    # I'm too lazy to do joystick presses in a thread or something)
    while not sound_player.is_sound_done_playing():
        if joy.is_button_pressed(0.1):
            sound_player.stop_playing()
            return True

    # wait for timeout_seoncs seconds before giving up. Return if a joystick button was pressed
    return joy.is_button_pressed(timeout_seconds)


while True:
    # wait for granny to press a button
    joy.wait_for_button_press()

    # let granny know what to do
    sound_player.play_sound_blocking(SOUND_PRESS_WHEN_YOU_HEAR_THE_RIGHT_PERSON)
    time.sleep(2)

    # loop through all contacts, play their sounds, and wait for joystick press
    for contact in contacts:
        if play_and_wait_for_button_press(contact.sound_filename, 3):
            # ask for confirumation
            if play_and_wait_for_button_press(SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_1, 0) or \
                    play_and_wait_for_button_press(contact.sound_filename, 0) or \
                    play_and_wait_for_button_press(SOUND_ARE_YOU_SURE_YOU_WANT_TO_CALL_PART_2, 3):
                dial(contact.phone_number)
            else:
                sound_player.play_sound_blocking(SOUND_DID_NOT_DIAL_BECAUSE_YOU_DID_NOT_CONFIRM)
            break

        sound_player.play_sound_blocking(SOUND_NO_CONTACT_SELECTED)
