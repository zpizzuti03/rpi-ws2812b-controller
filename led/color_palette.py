"""
color_palette.py

This module defines a color palette class which stores the
colors to apply to the LED strips.
"""
from dataclasses import dataclass
from .colors import COLORS, OFF, is_valid_color

@dataclass(slots=True)
class ColorPalette:
	"""
	Represents a validated color palette to be applied to LEDs on the strip

	This object:
		- Stores data on the selection of colors for the LED display
		- Holds four colors, a primary and secondary for the span of the led strip, and the spacing between
		- Validates all colors passed are valid else sets defaults
		- Can return each color
	"""
	span_primary : tuple[int, int, int] = OFF
	span_secondary : tuple[int, int, int] = OFF
	spacing_primary : tuple[int, int, int] = OFF
	spacing_secondary : tuple[int, int, int] = OFF

	def __post_init__(self):
		"""
		Performs validation on the values entered, and sets defaults if they are invalid
		"""
		self.validate_color("Span-Primary", self.span_primary)
		self.validate_color("Span-Secondary", self.span_secondary)
		self.validate_color("Spacing-Primary", self.spacing_primary)
		self.validate_color("Spacing-Secondary", self.spacing_secondary)

	def get_span_primary(self) -> tuple[int, int, int]:
		"""
		Returns the span's primary color
		"""
		return self.span_primary

	def get_span_secondary(self) -> tuple[int, int, int]:
		"""
		Returns the span's secondary color
		"""
		return self.span_secondary

	def get_space_primary(self) -> tuple[int, int, int]:
		"""
		Returns the spacing's primary color
		"""
		return self.spacing_primary

	def get_space_secondary(self) -> tuple[int, int, int]:
		"""
		Returns the spacing's secondary color
		"""
		return self.spacing_secondary

	@staticmethod
	def validate_color(name: str, color: tuple[int, int, int]):
		if not is_valid_color(color):
			raise ValueError(f"Invalid color for {name}: {color}")
