# controller.py
# This file maintains control over led hardware and orchestrates the changing of pixels
# Monitors and controls runtime state (i.e. current_color, etc.) 
import board 
import neopixel 
from . import config

pixels = neopixel.NeoPixel(config.PIN, config.LED_COUNT, brightness=config.DEFAULT_BRIGHTNESS)

def set_color(color):
        pixels.fill(color)

def set_brightness(val):
        pixels.brightness = val


def power_off():
	pixels.fill((0, 0, 0))
	pixels.show()


def power_all():
	pixels.show()
