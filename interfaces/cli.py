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
	controller.set_color = (COLORS["off"])
	controller.power_all()

if args.Red:
	print("Red")
	controller.set_color(COLORS["red"])
	controller.power_all() 

if args.Green:
	print("Green")
	controller.set_color(COLORS["green"])
	controller.power_all() 

if args.Blue:
	print("Blue")
	controller.set_color(COLORS["blue"])
	controller.power_all() 

if args.White:
	print("White")
	controller.set_color(COLORS["white"])
	controller.power_all() 
