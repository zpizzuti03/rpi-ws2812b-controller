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

	def max_spacing(self) -> int:
		"""
		Returns the maximum spacing a user is allowed to use on a given PixelRange
		"""
		length = self.end - self.start
		return max(0, range - self.span)        # User cannot make spacing greater than the span

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

	def is_in_span(self, index) -> bool:
		"""
		Returns true if the index provided is within the span length, or false if in spacing area

		index -- The index of the LED to be checked
		"""
		offset_index = index - self.start

		return (offset_index % self.get_period()) < self.span 

	def get_length(self):
		"""
		Returns the range which pixels will be lit up in based on inversion
		"""
		if not self.invert:
			return range(self.start, self.end, 1)
		return range(self.end - 1, self.start - 1, -1)

	def is_default(obj) -> bool:
		"""
		Checks the object's state to see if it matches a sentinel instance

		Returns true if is the same as the sentinel instance.
		"""
		return obj == _DEFAULT_RANGE_

	def has_spacing(self) -> bool:
		"""
		Returns true if spacing is any greater than 0.
		"""
		return self.spacing != 0

_DEFAULT_RANGE_ = PixelRange()	# Sentinel Value for checking state
