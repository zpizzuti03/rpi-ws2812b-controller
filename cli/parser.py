"""
This module defines the command-line argument parser for the LED Controller CLI

This module does not execute application logic, it is solely responsible
for constructing the argparse.ArgumentParser instance.

The parser returned is intended for use at the CLI entry point,
but may also be reused in devtools for testing
"""

import argparse

def build_parser():
	"""
	Construct and configure the CLI argument parser.

	Returns:
		argparse.ArgumentParser: A fully configured parser containing
		all command line options for the LED controller
	"""

	parser = argparse.ArgumentParser()

	parser.add_argument(
		"-o",
		"--off",
		action='store_true',
		help="Turn the lights off. Usage: '--off'"
	)

	parser.add_argument(
		"-c",
		"--color",
		nargs="+",
		metavar="COLOR",
		default=None,
		help="Primary color (span color): name/letter (r, red) or RGB (255,0,0). Usage: '--color r' '--color 255 0 0'. Color options: (red, blue, green, yellow, magenta, cyan, white)"
	)

	parser.add_argument(
		"--secondary-color",
		nargs="+",
		metavar="COLOR",
		default=None,
		help="Secondary color if supported: name/letter (r, red) or RGB (255,0,0). Usage: '--secondary-color r' '--secondary-color 255 0 0'"
	)

	parser.add_argument(
		"--spacing-color",
		metavar="COLOR",
		nargs="+",
		default=None,
		help="Spacing color (fills in non span spacing): name/letter (r, red) or RGB (255,0,0). Usage: '--spacing-color r' '--spacing-color 255 0 0'"
	)

	parser.add_argument(
		"--spacing-color-secondary",
		metavar="COLOR",
		nargs="+",
		default=None,
		help="Secondary spacing color (if secondary color is supported): name/letter (r, red) or RGB (255,0,0). Usage: '--spacing-color-secondary r' '--spacing-color-secondary 255 0 0'"
	)

	action_group = parser.add_mutually_exclusive_group()

	action_group.add_argument(
		"-f",
		"--fill",
		action='store_true',
		help="Fills the entire light strip with a specified color. Usage: '--fill'"
	)

	action_group.add_argument(
		"-b",
		"--blink",
		action='store_true',
		help="Blinks the entire light strip. Usage: '--blink' changes color every 1 second for 10 seconds by default, to edit see '--interval' and '--duration'"
	)

	action_group.add_argument(
		"-p",
		"--progressive",
		action='store_true',
		help="Progressively fills the light strip's LEDs, over an interval or duration. Duration wins precedence over interval, for more see '--interval' or '--duration'. Usage: '--progressive'"
	)

	action_group.add_argument(
		"-C",
		"--chase",
		action='store_true',
		help="Creates a bar of span length to chase itself back and forth on the LED strip. Usage: '--chase'"
	)

	parser.add_argument(
		"-s",
		"--span",
		type=int,
		help="Specifies a length for a span of LEDs. A span is a stretch of LEDs before spacing. This flag does nothing if not used with spacing. Usage: '--span 30'. This example means there will be 30 LEDs lit up before placing spacing between"
	)

	parser.add_argument(
		"-S",
		"--spacing",
		type=int,
		help="Specifies a number of LEDs to space between each span. Defaults to 0. Usage: '--spacing 4' will add four LEDs of spacing between each span"
	)

	parser.add_argument(
		"-I",
		"--invert",
		action='store_true',
		help="Specifies whether to fill starting from the beginning or end of the LED strip. Usage: '--invert'"
	)

	parser.add_argument(
		"-i",
		"--interval",
		type=float,
		help="Specifies and interval of time between effects, such as switching from one color to another. To control duration of the entire effect, see '--duration'. Usage: '--interval 0.5'"
	)

	parser.add_argument(
		"-d",
		"--duration",
		type=float,
		help="Specifies the duration of a timed effect. Defaults to 10 seconds if the flag is unused. To control the time between effects see '--interval'. Usage: '--duration 25'"
	)

	parser.add_argument(
		"-B",
		"--brightness",
		type=float,
		help="Sets the brightness of the light strip to a value between 0 and 1. Usage: '--brightness 0.5'"
	)

	parser.add_argument(
		"-R",
		"--range",
		type=int,
		nargs=2,
		metavar=("START", "END"),
		help="Sets the range from of lights to be altered (0-LED_COUNT). Usage: '--range 40 50'"
	)

	return parser
