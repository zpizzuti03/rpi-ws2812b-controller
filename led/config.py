"""
config.py

Configuration values for the LED controller system.

This module centralizes hardware configuration and default runtime
parameters for the LED strip.
"""
import board
import neopixel

PIN = board.D18
"""Defines the GPIO pin which the LED data wire is connected to on the board"""

LED_COUNT = 60
"""The number of LEDs to power on the strip to power, typically set to the number of LEDs on the strip"""

PIXEL_ORDER = neopixel.RGB
"""Defines which pixel order to use (e.g. RGB, GRB, etc.)"""

DEFAULT_BRIGHTNESS = 0.5
"""Defines the default brightness of the pixels"""
