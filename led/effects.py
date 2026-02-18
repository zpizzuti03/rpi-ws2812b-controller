"""
effects.py

Animation layer for the LED controller system.

This module defines time-based and pattern-based lighting effects
that operate on the LED strip through the controller module.
"""
from .controller import fill_color, fill_single, fill_range, power_off, set_brightness, show_pixels
from .colors import COLORS
from .config import LED_COUNT
from .timer import RepeatingTimer


def show_fill(color, start=0, end=LED_COUNT):
	"""
	Takes a user-specified color and fills the LED strip with it  

	Utilizes either fill_color if there is no specified range, or
	fill_range if there is a specified range to optimize filling

	Keyword arguments:
	color -- An RGB int tuple defining the color to change the LED strip to
	start -- the starting index of the fill area, defaults to the start 
	end -- the ending index of the fill area, defaults to the end 
	"""
	if start != 0 or end != LED_COUNT:
		fill_range(color, start, end)
	else:
		fill_color(color)
	show_pixels()


def blink_color(color, interval, start=0, end=LED_COUNT):
        """
        Takes a color and a a interval to blink a specfic color over an interval of time

        This function takes the color passed and uses a closure to encapsulate it into an
        action that can be passed to the repeating timer's action function. The timer updates
        and performs the blink and then this function alternates it's on state.

        Keyword arguments:
        color -- the color to flash when the LED strip is on
        interval -- the time in seconds which the light switches from on to off and vice-versa
        start -- 
	end -- 
	"""
        on = True

        def blink():
                nonlocal on
                show_fill(color if not on else COLORS["off"], start, end)
                on = not on

        timer = RepeatingTimer(interval, blink)

        while True:
                timer.update()

def progressive_fill(color):
	"""
	"""
	
