# cli.py
# This file parses command line arguments into actions for the led strip
import argparse
import string
from led import effects
from led.controller import power_off, set_brightness
from led.colors import COLORS, resolve_color

parser = argparse.ArgumentParser()

color_group = parser.add_mutually_exclusive_group(required=True)

color_group.add_argument("-o", "--off", action='store_true', help="Turn the lights off. Usage: '--off'")
color_group.add_argument("-c", "--color", type=str, help="Select a color from a using its first letter or name (r,g,b,w,y,c,m). Usage: '--color r'")
color_group.add_argument("-r", "--rgb", type=int, nargs=3, help="Select a color using a standard RGB value. Usage: '--rgb 255 0 0'")

action_group = parser.add_mutually_exclusive_group(required=True)

action_group.add_argument("-f", "--fill", action='store_true', help="Fills the entire light strip with a specified color. Usage: '--fill'")
action_group.add_argument("-s", "--blink", type=float, help="Blinks the entire light strip at a rate of time specified by a float value Usage: '--blink 1', '--blink 2.5'")
action_group.add_argument("-i", "--interval", help="During development, being used to test any function requiring an interval via cli", type=int) 

parser.add_argument("-b", "--brightness", type=float, help="Sets the brightness of the light strip to a value between 0 and 1. Usage: '--brightness 0.5'")

args = parser.parse_args()

resolved_color = resolve_color(args.rgb, args.color)


# ---- MUTALLY EXCLUSIVE COLOR ARGS ----

if args.off:
	print("Off")
	power_off()


if args.color:
	print(resolved_color)

if args.rgb:
	print(resolved_color)

# ---- EFFECT ARGS ----

if args.brightness:
	if(args.brightness >= 0 and args.brightness <= 1):
		set_brightness(args.brightness)
	else:
		print("Use a valid brightness between 0-1")

# Leave this as a test function,  seperate to a -b flag (blink)
if args.interval:
	print("interval")
	if args.interval is not None:
		effects.blink_color(args.interval)
	else:
		print("args.interval needs a value")

if args.fill:
	print("Filled")
	effects.show_fill(resolved_color)

if args.blink:
	print("Blinking")
	effects.blink_color(resolved_color, args.blink)
