"""
exit_codes.py

This module provides values for exit codes for the cli
"""
from enum import IntEnum

class ExitCode(IntEnum):
	SUCCESS = 0
	INVALID_INPUT = 1
