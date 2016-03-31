import pygame
import time

POLL_INTERVAL_SECONDS = 0.05


class Joystick:
    """Abstraction of a joystick."""
    def __init__(self):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def wait_for_button_press(self, timeout_in_seconds=-1):
        while timeout_in_seconds == -1 or timeout_in_seconds > 0:
            if self.is_button_currently_pressed():
                # first wait until no buttons are pressed anymore (to prevent double presses)
                while self.is_button_currently_pressed():
                    pass

                return True

            time.sleep(POLL_INTERVAL_SECONDS)

            if timeout_in_seconds != -1:
                timeout_in_seconds -= POLL_INTERVAL_SECONDS

        return False

    def is_button_currently_pressed(self):
        pygame.event.pump()
        for i in range(0, self.joystick.get_numbuttons()):
            if self.joystick.get_button(i) != 0:
                return True
        return False
