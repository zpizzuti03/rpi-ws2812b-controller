"""
effects.py

Animation layer for the LED controller system.

This module defines time-based and pattern-based lighting effects
that operate on the LED strip through the controller module.
"""
import queue
from .controller import fill_color, fill_single, fill_range, power_off, set_brightness, show_pixels
from .colors import COLORS
from .config import LED_COUNT
from .timer import RepeatingTimer
from .types import PixelRange

def show_fill(color, sel=PixelRange()):
	"""
	Takes a user-specified color and fills the LED strip with it  

	Utilizes either fill_color if there is no specified range, or
	fill_range if there is a specified range to optimize filling

	Keyword arguments:
	color -- An RGB int tuple defining the color to change the LED strip to
	sel -- A container with information on which pixels to display
	"""
	if not sel.is_default():
		fill_range(color, sel)
	else:
		fill_color(color)
	show_pixels()


def blink_color(color, interval=1, duration=10, sel=PixelRange()):
        """
        Takes a color and a a interval to blink a specfic color over an interval of time

        This function takes the color passed and uses a closure to encapsulate it into an
        action that can be passed to the repeating timer's action function. The timer updates
        and performs the blink and then this function alternates it's on state.

        Keyword arguments:
        color -- An RGB int tuple defining the color to blink on the LED strip
	duration -- A time in seconds which the blinking affect will run for
        interval -- the time in seconds which the light switches from on to off and vice-versa
        sel -- A container with information on which pixels to display
	"""
        on = True

        def blink():
                nonlocal on
                show_fill(color if not on else COLORS["off"], sel)
                on = not on

        timer = RepeatingTimer(interval, blink)

        while timer.get_runtime() <= duration:
                timer.update()

def progressive_fill(color, interval=1, sel=PixelRange()):
	"""
	Takes a color and optional range arguments to fill the LED strip one at a time from either direction

	Keyword arguments:
	color -- An RGB int tuple defining the color to progressively fill the LED strip with
	sel -- A container with information on which pixels to display
	"""
	leds_to_light = queue.Queue()

	for i in sel.range():
		leds_to_light.put(i)

	def prog_fill():
		nonlocal leds_to_light
		fill_single(color, leds_to_light.get())

	timer = RepeatingTimer(interval, prog_fill)

	while not leds_to_light.empty():
		timer.update()
