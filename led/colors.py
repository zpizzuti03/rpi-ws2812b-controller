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
}


def is_rgb_tuple(color):
	"""
	Determines if a given color is a tuple of 3 int rgb values

	Keyword arguments:
	color -- the color to be verified
	"""
	if type(color) is tuple:
		return True
	else:
		print("The color that was entered is not a valid RGB tuple)")
		return False


def resolve_color(rgb: list[int] | None, color: str | None) -> tuple[int, int, int]:
        """
        Takes an rgb value or string value and returns it as a tuple

        Takes either an rgb value as a list of 3 integers and returns a tuple
        generated from the integers, or a string value, and checks if it is
        contained in the list of defined colors and returns its key as a tuple. 

        Keyword arguments:
        rgb -- a list of three ints
        color -- a string value representing a key in the color dictionary.
        """
        if rgb is not None:
                return tuple(rgb)

        if color is not None:
                color = color.lower()
                # Determine if the color is in the dictionary
                if color in COLORS:
                        return tuple(COLORS[color])
                else:
                        print("Error: Please use a valid color from the list: (r,g,b,w,y,c,m)" )
        return (0, 0, 0)
