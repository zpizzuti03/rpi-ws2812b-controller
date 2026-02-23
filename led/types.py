"""
types.py

This module defines types to unify data collection
"""
from dataclasses import dataclass
from .config import LED_COUNT
from .colors import COLORS, OFF, is_valid_color

@dataclass(slots=True)
class ColorPalette:
	"""
	Represents a validated color palette to be applied to LEDs on the strip

	This object:
		- Stores data on the selection of colors for the LED display
		- Validates all colors passed are valid else sets defaults
		- Can return each color
	"""
	span_primary : tuple[int, int, int] = COLORS["red"]
	span_secondary : tuple[int, int, int] = OFF
	spacing_primary : tuple[int, int, int] = OFF
	spacing_secondary : tuple[int, int, int] = OFF

	def __post_init__(self):
		"""
		Performs validation on the values entered, and sets defaults if they are invalid
		"""
		self.span_primary = OFF if not is_valid_color(self.span_primary) else self.span_primary
		self.span_secondary = OFF if not is_valid_color(self.span_secondary) else self.span_secondary
		self.spacing_primary = OFF if not is_valid_color(self.spacing_primary) else self.spacing_primary
		self.spacing_secondary = OFF if not is_valid_color(self.spacing_secondary) else self.spacing_secondary

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


@dataclass(slots=True)
class PixelRange:
	"""
	Represents a validated selection of LEDs on the strip

	This object:
		- Stores the data on a selection of LEDs from the display
		- Validates the start, end, span, and spacing input values by clamping
		- Can return it's range based on inversion.
	"""
	start: int = 0			# The start boundary of the range to be filled
	end: int = LED_COUNT		# The end boundary of the range to be filled
	span: int = 1			# The length of each stretch of LEDs separated by spaces
	spacing: int = 0		# The space between each span of LEDs
	invert: bool = False		# A boolean defining whether to start lighting from the start or end of the strip

	def __post_init__(self):

		self.start = max(0, min(self.start, LED_COUNT)) if self.start is not None else 0
		self.end = max(0, min(self.end, LED_COUNT)) if self.end is not None else LED_COUNT

		range = self.end - self.start

		self.span = max(1, min(self.span, range)) if self.span is not None else 1
		self.spacing = max(0, min(self.spacing, range - self.span)) if self.spacing is not None else 0

	def get_length(self):
		"""
		Returns the range which pixels will be lit up in based on inversion
		"""
		if not self.invert:
			return range(self.start, self.end, 1)
		return range(self.end - 1, self.start - 1, -1)

	def is_in_span(self, index) -> bool:
		"""
		Returns true if the index provided is within the span length, or false if in spacing area

		index -- The index of the LED to be checked
		"""
		offset_index = index - self.start if not self.invert else (self.end - 1) - index

		return (offset_index % self.get_period()) < self.span

	def get_index_col(self, index, span_col=None, space_col=None) -> tuple[int, int, int]:
		"""
		Returns one of two provided colors

		Keyword arguments:
		index -- The index of the pixel to check
		span_col -- An RGB value representing the coloring for the span
		space_col -- An RGB value representing the coloring for the spacing
		"""
		if self.has_spacing() and not self.is_in_span(index):
			return space_col
		return span_col

	def get_span(self) -> int:
		"""
		Returns the value of the range's span
		"""
		return self.span

	def get_spacing(self) -> int:
		"""
		Returns the value of the range's spacing
		"""
		return self.spacing

	def get_period(self) -> int:
		"""
		Returns the length of one period (the length of one span and one unit of spacing)
		"""
		return self.get_span() + self.get_spacing()

	def max_spacing(self) -> int:
		"""
		Returns the maximum spacing a user is allowed to use on a given PixelRange
		"""
		length = self.end - self.start
		return max(0, range - self.span)# User cannot make spacing greater than the remaining space

	def has_spacing(self) -> bool:
		"""
		Returns true if spacing is any greater than 0.
		"""
		return self.spacing != 0

	def is_default(obj) -> bool:
		"""
		Checks the object's state to see if it matches a sentinel instance

		Returns true if is the same as the sentinel instance.
		"""
		return obj == _DEFAULT_RANGE_

_DEFAULT_RANGE_ = PixelRange()	# Sentinel Value for checking state
