"""
test_color_palette.py

This module verifies that default values apply
correctly to the ColorPalette dataclass and that invalid
values are rejected
"""
import pytest
from led.color_palette import ColorPalette
from led.colors import COLORS, OFF

@pytest.mark.parametrize("function", [
	"get_span_primary",
	"get_span_secondary",
	"get_space_primary",
	"get_space_secondary"
])
def test_default_color_palette(function):
	"""
	Tests that a default ColorPalette object returns the expected values
	"""
	p = ColorPalette()

	assert getattr(p, function)() == OFF

@pytest.mark.parametrize("field, value", [
	("span_primary", "invalid"),
	("span_secondary", "invalid"),
	("spacing_primary", "invalid"),
	("spacing_secondary", "invalid")
])
def test_color_palette_invalid_colors(field, value):
	"""
	Tests that a palette with invalid colors will throw errors
	"""
	with pytest.raises(ValueError):
		ColorPalette(**{field: value})
