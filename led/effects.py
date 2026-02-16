"""
effects.py

Animation layer for the LED controller system.

This module defines time-based and pattern-based lighting effects
that operate on the LED strip through the controller module.
"""
from .controller import fill_color, set_pixel_color, set_brightness, show_pixels
from .colors import COLORS
import time

def show_fill(color):
	"""
	Takes a user-specified color and fills the LED strip with it  

	Keyword arguments:
	color -- An RGB int tuple defining the color to change the LED strip to
	"""
	fill_color(color)
	show_pixels()


# blink_color allows for lights of a specified color to flash off and then back on again
# TODO: Seperate the time loop from the blink logic
def blink_color(interval):
	on = False
	next_update = time.monotonic()
	
	while True:
		next_update += interval

		fill_color(COLORS["green"] if not on else COLORS["off"])
		show_pixels()
		on = not on

		sleep_time = next_update - time.monotonic()
		if sleep_time > 0:
			time.sleep(sleep_time)

# TODO: blink_interval calls the blink_color function on a interval determined by a user for a user specified color.
