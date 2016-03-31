import sys
import pygame.mixer
from pygame.mixer import Sound


if sys.platform == "win32":
    # workaround in windows: windows won't play sounds if pygame.init() has been called (which we need for joystick to
    # work), but you can work around this bug by opening a window...
    # see http://stackoverflow.com/questions/2936914/pygame-sounds-dont-play
    pygame.init()
    screen = pygame.display.set_mode((40, 40), 0, 32)

class SoundPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(44100, -16, 2)
        self.currently_playing_sound = None

    def play_sound_blocking(self, filename):
        self.play_sound(filename)
        self.wait_for_sound_playing_done()

    def play_sound(self, filename):
        print "playing %s" % filename
        sound = Sound(filename)
        channel = sound.play()
        self.currently_playing_sound = {'sound': sound, 'channel': channel}

    def is_sound_done_playing(self):
        if self.currently_playing_sound is None:
            print "have not played anything yet!"
            return True
        return not self.currently_playing_sound['channel'].get_busy()

    def wait_for_sound_playing_done(self):
        while not self.is_sound_done_playing():
            pygame.time.delay(50)

    def stop_playing(self):
        if self.currently_playing_sound is None:
            print "stop playing? We have not played anything yet!"
            return
        self.currently_playing_sound['sound'].stop()
