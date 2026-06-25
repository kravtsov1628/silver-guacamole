import RPi.GPIO as GPIO

BUTTONS = {
    "UP": 6,
    "DOWN": 19,
    "LEFT": 5,
    "RIGHT": 26,
    "A": 13,
    "B": 21,
    "X": 20,
    "Y": 16,
    "START": 24,
    "SELECT": 12
}
GPIO.setmode(GPIO.BCM)
for pin in BUTTONS.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def pressed(button):
    return GPIO.input(BUTTONS[button]) == GPIO.LOW

def cleanup():
    GPIO.cleanup()