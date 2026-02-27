"""
types.py

This module defines the PixelRange data abstraction

PixelRange is a dataclass which holds the information on which 
arrangement of pixels to display on the LED strip, and how to arrange them
"""
from dataclasses import dataclass
from .config import LED_COUNT

@dataclass(slots=True)
class PixelRange:
	"""
	Represents a validated selection of LEDs on the strip.

	This object:
		- Stores the data on a selection of LEDs from the display
		- Validates the start, end, span, and spacing input values by clamping
		- Can provide information on the arrangement of pixels (e.g. range, color of a specific pixel, if an index is in the span)
	"""
	start: int = 0			# The start boundary of the range to be filled
	end: int = LED_COUNT		# The end boundary of the range to be filled
	span: int = 1			# The length of each stretch of LEDs separated by spaces
	spacing: int = 0		# The space between each span of LEDs
	invert: bool = False		# A boolean defining whether to start lighting from the start or end of the strip

	def __post_init__(self):

		self.set_start(self.start)
		self.set_end(self.end)

		self.set_span(self.span)
		self.set_spacing(self.spacing)

		self.set_invert(self.invert)

	def get_range(self):
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

	def get_start(self) -> int:
		"""
		Returns the value of the range's start
		"""
		return self.start

	def set_start(self, value: int) -> None:
		"""
		Sets or clamps the start value of the range to the value provided after validation
		"""
		if value is None:
			self.start = 0
		elif self.ensure_int(value, "start"):
			self.start = max(0, min(value, LED_COUNT))

	def get_end(self) -> int:
		"""
		Returns the value of the range's end
		"""
		return self.end

	def set_end(self, value: int) -> None:
		"""
		Sets or clamps the end value of the range to the value provided after validation
		"""
		if value is None:
			self.end = LED_COUNT
		elif self.ensure_int(value, "end"):
			self.end = max(1, min(value, LED_COUNT))

	def get_span(self) -> int:
		"""
		Returns the value of the range's span
		"""
		return self.span

	def set_span(self, value: int) -> None:
		"""
		Sets or clamps the span value of the range to the value provided after validation
		"""
		if value is None:
			self.span = 1
		elif self.ensure_int(value, "span"):
			self.span = max(1, min(value, self.get_length()))

	def is_inverted(self) -> bool:
		"""
		Returns true if the range is inverted or false if not
		"""
		return self.invert

	def set_invert(self, value: bool) -> None:
		"""
		Sets the inversion value as long as it is a boolean type
		"""

		if not isinstance(value, bool):
			raise TypeError(f"Value {value} provided for set_invert is not of type boolean")
		self.invert = value

	def get_spacing(self) -> int:
		"""
		Returns the value of the range's spacing
		"""
		return self.spacing

	def set_spacing(self, value: int) -> None:
		"""
		Sets or clamps the spacing value of the range to the value provided after validation
		"""
		if value is None:
			self.spacing = 0
		elif self.ensure_int(value, "spacing"):
			self.spacing = max(0, min(value, self.get_length() - self.span))


	def get_period(self) -> int:
		"""
		Returns the length of one period (the length of one span and one unit of spacing)
		"""
		return self.get_span() + self.get_spacing()

	def get_length(self) -> int:
		"""
		Returns the integer length of the range
		"""
		return self.end - self.start

	def max_spacing(self) -> int:
		"""
		Returns the maximum spacing a user is allowed to use on a given PixelRange
		"""
		length = self.end - self.start
		return max(0, range - self.span) # User cannot make spacing greater than the remaining space

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

	def ensure_int(self, value, function_name) -> bool:
		"""
		This function takes a value and verifies that it is an integer

		Returns true if value is an integer or raises a TypeError
		"""
		if not isinstance(value, int):
			raise TypeError(f"Value provided {value} for set_{function_name} is not of type integer.")
		return True

_DEFAULT_RANGE_ = PixelRange()	# Sentinel Value for checking state
