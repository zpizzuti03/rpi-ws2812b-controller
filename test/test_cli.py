"""
test_cli.py

Unit tests for the application's CLI entry point.

This module verifies CLI argument handling and return codes
for the main entry point.
"""
import pytest
from cli.__main__ import main

@pytest.mark.parametrize("flags", [
	(["--color", "g"]),
	(["--secondary-color", "g"]),
	(["--spacing-color", "g"]),
	(["--spacing-color-secondary", "g"])
])
def test_cli_color_options(flags):
	"""
	Tests that all color flags return successful when provided a valid value
	"""
	assert main(flags) == 0
