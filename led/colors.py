"""
colors.py

Defines a dictionary of named color mappings and color utility functions.

This module defines a dictionary of color mappings that contains both their 
first letter and full name as a key, as well as tools to properly create and
verify integer tuples for setting colors.

"""
COLORS = {
	"r": (255, 0, 0),
	"red": (255, 0, 0),

	"g": (0, 255, 0),
	"green": (0, 255, 0),

	"b": (0, 0, 255),
	"blue": (0, 0, 255),

	"w": (255, 255, 255),
	"white": (255, 255, 255),

	"y": (255,255,0),
	"yellow": (255,255,0),

	"c": (0, 255, 255),
	"cyan": (0, 255, 255),

	"m": (255,0,255),
	"magenta": (255,0,255),

	"off": (0, 0, 0),
}

OFF = COLORS["off"]

def is_valid_color(color) -> bool:
	"""
	Determines if a given color is a valid tuple of 3 int rgb values

	Keyword arguments:
	color -- the value to be verified as a color
	"""
	if isinstance(color, tuple) and len(color) == 3 and all(isinstance(x, int) for x in color):
		for x in color:
			if x < 0 or x > 255:
				return False
		return True
	return False


def resolve_color(color: str | list[int, int, int] | None) -> tuple[int, int, int]:
	"""
	Takes a list of input values and returns a vaild rgb tuple if within parameters

	Takes a list of input values and parses them to determine if it is a string
	contained in the COLORS dictionary and returns a tuple, OR if it is an RGB value, 
	parses and verifies that it is valid and returns the tuple.

	Keyword arguments:
	color -- a value representing a color through string or RGB.
	"""
	if color is not None:
		if isinstance(color, list) and len(color) == 1 and isinstance(color[0], str):
			# Check one string values
			name = color[0].lower()
			if name in COLORS:
				return tuple(COLORS[name])
			else:
				raise ValueError(f"Unknown color '{name}'. See options: ('red', 'green', 'blue', 'white', 'yellow', 'magenta', 'cyan')")
		elif isinstance(color, list) and len(color) == 3 and all(isinstance(x, str) for x in color):
			# Check RGB values
			try:
				rgb_tuple = tuple(int(x) for x in color)
			except(ValueError):
				raise ValueError("RGB Values must be integers.")

			if not is_valid_color(rgb_tuple):
				raise ValueError("RGB Values must be between 0 and 255.")

			return rgb_tuple
	else:
		raise ValueError(f"No color provided or Invalid color format: {color}")
