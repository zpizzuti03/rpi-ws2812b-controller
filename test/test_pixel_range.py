"""
test_types

This module verifies that default values apply
correctly to types and that their functions return expected results
"""
import pytest
from led.pixel_range import PixelRange
from led.config import LED_COUNT

MIN_RANGE = 0
MAX_RANGE = LED_COUNT
RANGE_TOO_LOW = -1
RANGE_TOO_HIGH = MAX_RANGE + 1

# ----- Pixel Range -----

@pytest.mark.parametrize("function, expected", [
	("get_start", MIN_RANGE),
	("get_end", MAX_RANGE),
	("get_span", 1),
	("get_spacing", 0),
	("is_inverted", False),
	("is_default", True)
])
def test_default_pixel_range(function, expected):
	"""
	Tests that a default PixelRange returns expected values
	"""
	r = PixelRange()

	assert getattr(r, function)() == expected

@pytest.mark.parametrize("field, original, expected", [
	("start", RANGE_TOO_LOW, MIN_RANGE),
	("start", RANGE_TOO_HIGH, MAX_RANGE),
	("end", RANGE_TOO_LOW, MIN_RANGE + 1),
	("end", RANGE_TOO_HIGH, MAX_RANGE),
])
def test_pixel_range_invalid_ranges(field, original, expected):
	"""
	Tests that invalid PixelRange args are processed properly
	"""
	r = PixelRange(**{field: original})

	actual = getattr(r, f"get_{field}")()

	assert actual == expected
	assert actual != original

@pytest.mark.parametrize("start, end", [
	(MIN_RANGE, MAX_RANGE),
	(MIN_RANGE, 50),
	(30, MAX_RANGE),
	(10, 40),
	(5, 55),
	(25, 35),
])
def test_pixel_range_inversion(start, end):
	"""
	Tests that inversion returns a valid inverted range
	"""
	r = PixelRange(start=start, end=end, invert=True)

	original = range(start, end)
	expected = range(end - 1, start - 1, -1)

	assert r.get_length() == expected
	assert r.get_length() != original

@pytest.mark.parametrize("index, expected", [
	(0, True),
	(2, True),
	(3, False),
	(4, False),
	(5, True),
	(7, True),
	(8, False)
])
def test_pixel_range_in_span(index, expected):
	"""
	Test values in a range and verify if they are in the span.

	Tests arbitrary values along a range with predetermined span and spacing 
	to determine whether they are located in the span or spacing
	"""
	r = PixelRange(span=3, spacing=2)

	assert r.is_in_span(index) == expected

@pytest.mark.parametrize("start, end, span, expected", [
	(MIN_RANGE, MAX_RANGE, MAX_RANGE, True),
	(MIN_RANGE, MAX_RANGE, RANGE_TOO_HIGH, False),
	(10, 20, 10, True),
	(10, 20, 11, False),
	(10, 20, -1, False)
])
def test_pixel_range_invalid_span(start, end, span, expected):
	"""
	Tests whether or not a span entered is valid or is clamped due to being out of range
	"""
	r = PixelRange(start=start, end=end, span=span)

	has_original_span = r.get_span() == span

	assert has_original_span == expected

@pytest.mark.parametrize("start, end, span, spacing, expected", [
	(MIN_RANGE, MAX_RANGE, 2, 2, True),
	(MIN_RANGE, MAX_RANGE, MAX_RANGE, 1, False),
	(2, 5, 3, 1, False),
	(2, 6, 3, 1, True),
	(20, 40, 19, 1, True),
	(48, 60, 12, 1, False),
])
def test_pixel_range_valid_spacing(start, end, span, spacing, expected):
	"""
	Tests invalid spacing arguments and ensures they are properly clamped in relation to span
	"""
	r = PixelRange(start=start, end=end, span=span, spacing=spacing)

	has_original_spacing = r.get_spacing() == spacing

	assert has_original_spacing == expected
