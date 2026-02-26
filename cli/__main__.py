"""
__main__.py

This module acts as the CLI entry point for the program
"""
import sys
from .parser import build_parser
from .commands import run_commands

def main(argv=None):
	"""
	The main entry point

	Keyword arguments:
	argv -- The arguments to be parsed and run as commands
	"""
	parser = build_parser()
	args = parser.parse_args(argv)
	return run_commands(args)


if __name__ =="__main__":
	sys.exit(main())
