"""
test_colors.py

Unit tests for led color resolutions

This module verifies that valid colors resolve
correctly and invalid colors throw exceptions
"""
import pytest
from led.colors import COLORS, OFF, is_valid_color, resolve_color

@pytest.mark.parametrize("test_value,expected", [
	(["r"], COLORS["red"]),
	(["green"], COLORS["green"]),
	(["B"], COLORS["blue"]),
	(["MAGENTA"], COLORS["magenta"]),
	(["255", "255", "255"], COLORS["white"])
])
def test_valid_colors(test_value, expected):
	"""
	Takes valid colors and asserts that they equal an expected result
	"""
	assert resolve_color(test_value) == expected


@pytest.mark.parametrize("value", [
	(["invalid"]),
	(["r", "g", "b"]),
	(None)
])
def test_invalid_color_string(value):
	"""
	Takes invalid colors and verifies they throw a ValueError
	"""
	with pytest.raises(ValueError):
		resolve_color(value)

@pytest.mark.parametrize("value", [
	(256, 0, 0),
	(-1, 0, 0),
	(0, 256, 0),
	(0, -1, 0),
	(0, 0, 256),
	(0, 0, -1)
])
def test_invalid_rgb_tuples(value):
	"""
	Takes an invalid rgb tuple and verifies that is_valid_color returns False
	"""
	assert is_valid_color(value) == False
