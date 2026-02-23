
"""
effects.py

Animation layer for the LED controller system.

This module defines time-based and pattern-based lighting effects
that operate on the LED strip through the controller module.
"""
import queue
from .controller import fill_color, fill_single, fill_range, power_off, set_brightness, show_pixels
from .colors import COLORS, OFF
from .timer import RepeatingTimer
from .types import ColorPalette, PixelRange

def validate_selections(palette, sel):
	"""
	Validates the color palette and selection, assigning defaults if they are None

	palette -- A container holding color reltated information for LED pixels
	sel -- A container with information on which pixels to display
	"""
	if palette is None:
		palette = ColorPalette()
	if sel is None:
		sel = PixelRange()
	return palette, sel

def fill_by_period(span_col=None, space_col=None, sel=None):
	"""
	Fills a range of selected pixels by the span length and spacing parameters specified

	Keyword arguments:
	span_col -- The color of the span length
	space_col -- The color to fill in spacing with. If none is provided, spacing is skipped
	sel -- A container with information on which pixels to display
	"""
	skip_spaces = False
	if span_col is None:
		span_col = OFF
	if space_col is None:
		skip_spaces = True	# If the color is None, don't even fill just skip
	if sel is None:
		sel = PixelRange()

	for i in sel.get_length():
		if sel.is_in_span(i):
			fill_single(index= i, color=span_col)
		elif not skip_spaces:
			fill_single(index=i, color=space_col)
		else:
			i += sel.get_spacing()

def fill_pixels(span_col=None, space_col=None, sel=None):
	"""
	Decides which method to fill pixels with based on user input and selections

	This function determines whether it is most efficient to fill by
	range, period, or all at once depending on the selecitons that the user has made.

	Keyword arguments:
	span_col -- An RGB int tuple defining the primary color to change the LED strip's span length to
	space_col -- An RGB int tuple defining the color of spacing (LEDs are OFF by default)
	sel -- A container with information on which pixels to display
	"""
	if sel.has_spacing():
		fill_by_period(span_col=span_col, space_col=space_col, sel=sel)
	elif not sel.is_default():
		fill_range(color=span_col, length=sel.get_length())
	else:
		fill_color(color=span_col)
	show_pixels()

def apply_fill(palette=None, sel=None):
	"""
	Wrapper function to apply filling to pixels with paramters that still must be verified

	palette -- A container holding color reltated information for LED pixels
	sel -- A container with information on which pixels to display
	"""
	palette, sel = validate_selections(palette=palette, sel=sel)
	fill_pixels(span_col=palette.get_span_primary(), space_col=palette.get_spacing_primary(), sel=sel)

def blink_color(palette=None, interval=None, duration=None, sel=None):
	"""
	Takes a color and a a interval to blink a specfic color over an interval of time

	This function takes the colors passed and uses a closure to encapsulate it into an
	action that can be passed to the repeating timer's action function. The timer updates
	and performs the blink and then this function alternates it's on state.

	Keyword arguments:
	palette -- A container holding color reltated information for LED pixels
	interval -- the time in seconds which the light switches from color1 to color2
	duration -- A time in seconds which the blinking affect will run for
	sel -- A container with information on which pixels to display
	"""
	palette, sel = validate_selections(palette=palette, sel=sel)
	if interval is None:
		interval = 1
	if duration is None:
		duration = 10

	on = True

	def blink():
		nonlocal on
		fill_pixels(span_col=palette.get_span_primary() if not on else palette.get_span_secondary(),
			space_col=palette.get_spacing_primary() if not on else palette.get_spacing_secondary(), sel=sel)
		on = not on

	timer = RepeatingTimer(interval, blink)

	while timer.get_runtime() <= duration:
		timer.update()

def progressive_fill(palette=None, interval=None, duration=None, sel=None):
	"""
	Takes a color and optional range arguments to fill the LED strip one at a time from either direction

	Keyword arguments:
	palette -- A container holding color reltated information for LED pixels
	interval -- The interval of time between each light turning on
	duration -- The duration of the effect, will calculate the interval of time based on leds
	sel -- A container with information on which pixels to display
	"""
	palette, sel = validate_selections(palette=palette, sel=sel)

	leds_to_light = queue.Queue()

	for i in sel.get_length():
		leds_to_light.put(i)

	# Duration mode wins precedence over interval mode
	if duration is not None:
		interval = duration / leds_to_light.qsize()

	if interval is None and duration is None:
		interval = 1

	def prog_fill():
		nonlocal leds_to_light
		fill_single(color=palette.get_span_primary(), index=leds_to_light.get())

	timer = RepeatingTimer(interval, prog_fill)

	while not leds_to_light.empty():
		timer.update()
