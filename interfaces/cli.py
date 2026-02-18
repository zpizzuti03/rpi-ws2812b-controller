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

parser = argparse.ArgumentParser()

color_group = parser.add_mutually_exclusive_group(required=True)

color_group.add_argument("-o", "--off", action='store_true', help="Turn the lights off. Usage: '--off'")
color_group.add_argument("-c", "--color", type=str, help="Select a color from a using its first letter or name (r,g,b,w,y,c,m). Usage: '--color r'")
color_group.add_argument("-r", "--rgb", type=int, nargs=3, help="Select a color using a standard RGB value. Usage: '--rgb 255 0 0'")

action_group = parser.add_mutually_exclusive_group(required=True)

action_group.add_argument("-f", "--fill", action='store_true', help="Fills the entire light strip with a specified color. Usage: '--fill'")
action_group.add_argument("-b", "--blink", type=float, help="Blinks the entire light strip at a rate of time specified by a float value Usage: '--blink 1', '--blink 2.5'")

parser.add_argument("-B", "--brightness", type=float, help="Sets the brightness of the light strip to a value between 0 and 1. Usage: '--brightness 0.5'")
parser.add_argument("-R", "--range", type=int, nargs=2, help="Sets the range from of lights to be altered (0-LED_COUNT). Usage: '--range 40 50'")

args = parser.parse_args()

resolved_color = resolve_color(args.rgb, args.color)

start = 0
end = LED_COUNT

# ---- MUTALLY EXCLUSIVE COLOR ARGS ----

if args.off:
	print("Off")
	power_off()


if args.color:
	print(resolved_color)

if args.rgb:
	print(resolved_color)

# ---- OPTION ARGS ----

if args.range:
	start, end = args.range
	print(start)
	print(end)

	if start < 0:
		start = 0
	if end > LED_COUNT:
		end = LED_COUNT

if args.brightness:
	if(args.brightness >= 0 and args.brightness <= 1):
		set_brightness(args.brightness)
	else:
		print("Use a valid brightness between 0-1")

# ---- EFFECT ARGS ----

if args.blink:
	print("Blinking")
	effects.blink_color(resolved_color, args.blink)

if args.fill:
	print("Filled")
	effects.show_fill(resolved_color, start, end)
