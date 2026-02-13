# config.py
# Holds default values for the led controller
import board
import neopixel

# Defines the GPIO pin which the LED board is connected to
PIN = board.D18

# The number of LEDs to light on the strip, typically set to the maximum
LED_COUNT = 60

# Defines which pixel order to use (e.g. RGB, GRB, RGBW, etc.)
PIXEL_ORDER = neopixel.RGB

# Defines the default brightness of the pixels
DEFAULT_BRIGHTNESS = 0.5
