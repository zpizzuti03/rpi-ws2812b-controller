"""
commands.py

Command dispatcher for the LED control system.

This module translates parsed CLI arguments into
LED actions by calling effects and controller functions. 
"""
from led import effects
from led.controller import power_off, set_brightness
from led.colors import resolve_color, OFF
from led.color_palette import ColorPalette
from led.pixel_range import PixelRange
from .exit_codes import ExitCode

def run_commands(args=None):
	"""
	Executes LED operations based on parsed command-line arguments

	This function interprets passed argparse input and
	executes the effect or function associated with the
	command. This effectively serves as a user input 
	command routing layer.

	Keyowrd arguments:
	args -- Parsed command line arguments. If None are provided, polled through sys.argv.

	Returns:
	int value representing exit status code (0 for success, non-zero for failiure)
	"""
	# --- POWER OFF ----

	if args.off:
		print("Off")
		power_off()
		return ExitCode.SUCCESS

	# Create a range object to store data
	try:
		selection = PixelRange(
			start=args.range[0] if args.range else None,
			end=args.range[1] if args.range else None,
			span=args.span if args.span else None,
			spacing=args.spacing if args.spacing else None,
			invert=args.invert
		)
	except TypeError as e:
		print(f"[ERROR] {e}")
		return ExitCode.INVALUD_INPUT

	# ---- COLOR ARGS ----

	if args.color is not None:
		try:
			primary_color = resolve_color(args.color)
		except ValueError as e:
			print(f"[ERROR] [PRIMARY-COL]: {e}")
			return ExitCode.INVALID_INPUT
		print(f"Primary color: {primary_color}")
	else:
		primary_color = OFF

	if args.secondary_color is not None:
		try:
			secondary_color = resolve_color(args.secondary_color)
		except ValueError as e:
			print(f"[ERROR] [SECONDARY-COL]: {e}")
			return ExitCode.INVALID_INPUT
		print(f"Secondary color: {secondary_color}")
	else:
		secondary_color = OFF

	if args.spacing_color is not None:
		try:
			spacing_color = resolve_color(args.spacing_color)
		except ValueError as e:
			print(f"[ERROR] [SPACING-PRIMARY-COL]: {e}")
			return ExitCode.INVALID_INPUT
		print(f"Spacing color: {spacing_color}")
	else:
		spacing_color = OFF

	if args.spacing_color_secondary is not None:
		try:
			spacing_color_secondary = resolve_color(args.spacing_color_secondary)
		except ValueError as e:
			print(f"[ERROR] [SPACING-SECONDARY-COL]: {e}")
			return ExitCode.INVALID_INPUT
		print(f"Spacing secondary color: {spacing_color_secondary}")
	else:
		spacing_color_secondary = OFF

	# Construct the Color Palette
	try:
		colors = ColorPalette(
			span_primary=primary_color,
			span_secondary=secondary_color,
			spacing_primary=spacing_color,
			spacing_secondary=spacing_color_secondary
		)
	except ValueError as e:
		print(f"[ERROR]: {e}")
		return ExitCode.INVALID_INPUT

	# ---- OPTION ARGS ----

	if args.interval is not None and args.interval <= 0:
		print(f"Interval {args.interval} is invalid, interval must be greater than 0 seconds")
		return ExitCode.INVALID_INPUT

	if args.duration is not None and args.duration <= 0:
		print(f"Duration {args.duration} is invalid, duration must be greater than 0 seconds")
		return ExitCode.INVALID_INPUT

	if args.brightness is not None:
		if(args.brightness >= 0 and args.brightness <= 1):
			set_brightness(args.brightness)
		else:
			print("Use a valid brightness between 0-1")

	# ---- EFFECT ARGS ----

	if args.chase:
		print("Chase")
		effects.chase_fill(
			palette=colors,
			interval=args.interval,
			duration=args.duration,
			sel=selection
		)

	if args.progressive:
		print("Progressive")
		if args.interval is not None and args.duration is not None:
			print("Note: Both --interval and --duration were provided. --duration takes precedence and will override --interval.")
		elif args.interval is None and args.duration is None:
			print("No --interval or --duration specified. Using default interval: 1 second.")
		effects.progressive_fill( 
			palette=colors,
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
			palette=colors,
			interval=args.interval,
			duration=args.duration,
			sel=selection
		)

	if args.fill:
		print("Filled")
		effects.apply_fill(
			palette=colors,
			sel=selection
		)

	return ExitCode.SUCCESS
