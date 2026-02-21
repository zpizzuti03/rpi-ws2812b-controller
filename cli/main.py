"""
main.py

This module parses command line arguments into actions for the LED strip
"""
import sys
import argparse
import string
from led import effects
from led.controller import power_off, set_brightness
from led.colors import resolve_color
from led.types import PixelRange
from .parser import build_parser

def main(argv=None):
	parser = build_parser()
	args = parser.parse_args(argv)

	# --- POWER OFF ----

	if args.off:
		print("Off")
		power_off()
		return 0

	# Create a range object to store data
	selection = PixelRange(
		start=args.range[0] if args.range else None,
		end=args.range[1] if args.range else None,
		span=args.span if args.span else None,
		spacing=args.spacing if args.spacing else None,
		invert=args.invert
	)

	# ---- COLOR ARGS ----

	if args.color is not None:
		try:
			primary_color = resolve_color(args.color)
		except ValueError as e:
			print(f"[ERROR] [PRIMARY-COL]: {e}")
			return 1
		print(f"Primary color: {primary_color}")
	else:
		primary_color = None

	if args.secondary_color is not None:
		try:
			secondary_color = resolve_color(args.secondary_color)
		except ValueError as e:
			print(f"[ERROR] [SECONDARY-COL]: {e}")
			return 1
		print(f"Secondary color: {secondary_color}")
	else:
		secondary_color = None

	if args.spacing_color is not None:
		try:
			spacing_color = resolve_color(args.spacing_color)
		except ValueError as e:
			print(f"[ERROR] [SPACING-PRIMARY-COL]: {e}")
		print(f"Spacing color: {spacing_color}")
	else:
		spacing_color = None

	if args.spacing_color_secondary:
		try:
			spacing_color_secondary = resolve_color(args.spacing_color_secondary)
		except ValueError as e:
			print(f"[ERROR] [SPACING-SECONDARY-COL]: {e}")
		print(f"Spacing secondary color: {spacing_color_secondary}")
	else:
		spacing_color_secondary = None

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
			span_col=primary_color,
			space_col=spacing_color,
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
			span_col_primary=primary_color,
			span_col_secondary=secondary_color,
			space_col_primary=spacing_color,
			space_col_secondary=spacing_color_secondary,
			interval=args.interval,
			duration=args.duration,
			sel=selection
		)

	if args.fill:
		print("Filled")
		effects.apply_fill(
			span_col=primary_color,
			space_col=spacing_color,
			sel=selection
		)

	return 0


if __name__ =="__main__":
	sys.exit(main())
