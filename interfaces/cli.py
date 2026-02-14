# cli.py
# This file parses command line arguments into actions for the led strip
import argparse
from led import controller
from led.colors import COLORS

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group()

group.add_argument("-o", "--Off", help="Turn all lights off", action='store_true')
group.add_argument("-r", "--Red", help="Turn all lights red with default settings", action='store_true')
group.add_argument("-g", "--Green", help="Turn all lights green with default settings", action='store_true')
group.add_argument("-b", "--Blue", help="Turn all lights blue with default settings", action='store_true')
group.add_argument("-w", "--White", help="Turn all lights white with default settings", action='store_true')

args = parser.parse_args()


if args.Off:
	print("Off")
	controller.power_off()

if args.Red:
	print("Red")
	controller.fill(COLORS["red"])
	controller.show_pixels() 

if args.Green:
	print("Green")
	controller.fill(COLORS["green"])
	controller.show_pixels() 

if args.Blue:
	print("Blue")
	controller.fill(COLORS["blue"])
	controller.show_pixels() 

if args.White:
	print("White")
	controller.fill(COLORS["white"])
	controller.show_pixels() 
