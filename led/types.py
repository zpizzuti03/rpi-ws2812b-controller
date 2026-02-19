"""
types.py

This module defines types to unify data collection
"""
from dataclasses import dataclass
from .config import LED_COUNT

@dataclass(slots=True)
class PixelRange:
	"""
	Represents a validated selection of LEDs on the strip

	This object stores the data on a selection of LEDs
	from the display, clamps the start and end values of the input
	in the event that invalid input is recieved, and has the
	capability to return a range based on inversion.
	"""
	start: int = 0
	end: int = LED_COUNT
	spacing: int = 1
	invert: bool = False
	max_spacing = LED_COUNT - 1

	def __post_init__(self):
		# Clamp the start and end values
		self.start = max(0, min(self.start, LED_COUNT))
		self.end = max(0, min(self.end, LED_COUNT))

		length = self.end - self.start
		max_spacing = max(1, length - 1)	# User cannot make spacing greater than specified length

		if self.spacing <= 0 or self.spacing > max_spacing:
			raise ValueError("spacing must be at least 1 less then the length of the range selected")

	def range(self):
		if not self.invert:
			return range(self.start, self.end, self.spacing)
		return range(self.end - 1, self.start - 1, -self.spacing)

	def is_default(obj):
		return obj == _DEFAULT_RANGE_

_DEFAULT_RANGE_ = PixelRange()	# Sentinel Value for checking state
