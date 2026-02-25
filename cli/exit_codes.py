"""
exit_codes.py

This module provides values for exit codes for the cli
"""
from enum import Enum

class ExitCode(Enum):
	SUCCESS = 0
	INVALID_INPUT = 1
