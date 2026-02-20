"""
cli.py

This module parses command line arguments into actions for the LED strip
"""
import argparse
import string
from led import effects
from led.controller import power_off, set_brightness
from led.colors import COLORS, resolve_color
from led.config import LED_COUNT
from led.types import PixelRange

def main():
	parser = argparse.ArgumentParser()

	# ---- Add parser arguments ----

	color_group = parser.add_mutually_exclusive_group()

	color_group.add_argument(
		"-o",
		"--off",
		action='store_true',
		help="Turn the lights off. Usage: '--off'"
	)

	color_group.add_argument(
		"-c",
		"--color",
		type=str,
		help="Select a color from a using its first letter or name (r,g,b,w,y,c,m). Usage: '--color r'"
	)

	color_group.add_argument(
		"-r",
		"--rgb",
		type=int,
		nargs=3,
		metavar=("R", "G", "B"),
		help="Select a color using a standard RGB value. Usage: '--rgb 255 0 0'"
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

	parser.add_argument(
		"-s",
		"--spacing",
		type=int,
		help="Specifies an interval for a range based fill, defaults to 1 (no skipping). Usage: '--interval 2'"
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

	args = parser.parse_args()

	# --- POWER OFF ----

	if args.off:
		print("Off")
		power_off()
		return


	# ---- Resolve color ----
	resolved_color = resolve_color(args.rgb, args.color)

	# Create a range object to store data
	selection = PixelRange(
		start=args.range[0] if args.range is not None else 0,
		end=args.range[1] if args.range is not None else LED_COUNT,
		spacing=args.spacing if args.spacing is not None else 1,
		invert=args.invert
	)

	# ---- COLOR ARGS ----

	if args.color:
		print(resolved_color)

	if args.rgb:
		print(resolved_color)

	# ---- OPTION ARGS ----

	if args.brightness:
		if(args.brightness >= 0 and args.brightness <= 1):
			set_brightness(args.brightness)
		else:
			print("Use a valid brightness between 0-1")

	# ---- EFFECT ARGS ----

	if args.progressive:
		print("Progressive")
		if args.interval is not None and args.duration is not None:
			print("Note: Both --interval and --duration were provided. --duration takes precedence and will override --interval.")
		elif args.interval is None and args.duration is None:
			print("No --interval or --duration specified. Using default interval: 1 second.")
		effects.progressive_fill( 
			color=resolved_color,
			interval=args.interval,
			duration=args.duration,
			sel=selection
		)

	if args.blink:
		print("Blinking")
		if args.interval is None:
			print("No --interval provided. Using default interval of 1 second.")
		if args.duration is None:
			print("No --duration provided. Using default duration of 10 seconds.")

		effects.blink_color(
			color=resolved_color,
			interval=args.interval,
			duration=args.duration,
			sel=selection
		)

	if args.fill:
		print("Filled")
		effects.show_fill(
			color=resolved_color,
			sel=selection
		)


if __name__ =="__main__":
	main()
