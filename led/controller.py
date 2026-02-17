"""
controller.py

Hardware abstraction layer for the LED strip

This module maintains provides control over the NeoPixel LED hardware.
 and orchestrates the changing of pixels
Monitors and controls runtime state (i.e. current color, brightness, etc.) 
"""
import board 
import neopixel 
from . import config
from .colors import COLORS, is_rgb_tuple

pixels = neopixel.NeoPixel(config.PIN, config.LED_COUNT, brightness=config.DEFAULT_BRIGHTNESS)

def fill_color(color):
	"""
	Fills the entire LED strip with a specified color

	Keyword arguments:
	color -- the color to fill the LED strip with
	"""
	if is_rgb_tuple(color):
		pixels.fill(color)

def set_pixel_color(index, color):
	"""
	Fills a single LED with a specified color by index

	Keyword arguments:
	index -- the index of the pixel on the LED strip (0-LED_COUNT)
	color -- the color to fill the pixel with
	"""
	if is_rgb_tuple(color):
		pixels[index].fill(color)

def set_brightness(val):
	"""
	Sets the brightness of the entire LED strip

	This function sets the brightness of the LEDs for the 
	entire strip. Note: the ws2812b LED strip this function is 
	designed for does not support individual LED brightness.

	Keyowrd arguments:
	val - the float value (0 to 1) to determine the brightness of the LEDs
	"""
	if val >= 0 and val <= 1:
	        pixels.brightness = val
	else:
		print("Please enter a brightness value between 0 and 1.")

def power_off():
	"""
	Turns off the all of the lights on the LED strip

	"""
	pixels.fill(COLORS["off"])
	pixels.show()

def show_pixels():
	"""
	Displays all updated information to the pixels on the board
	"""
	pixels.show()
