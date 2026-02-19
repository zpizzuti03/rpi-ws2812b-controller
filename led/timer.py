"""
timer.py

This module introduces an abstraction for a repeating timer which can
perform actions over a given interval using time.monotonic
"""
import time

class RepeatingTimer:
	"""
	This class defines the capabilities for a repeating timer which takes an action
	and performs it at an interval
	"""
	start_time = time.monotonic()
	next_update = start_time
	interval = 1
	action = None

	def __init__(self, interval=1, action=None):
		"""
		Initialize the repeating timer

		Keyword arguments:
		interval -- the interval over which to repeat a function
		action -- the function of the action to be repeated over an interval
		"""
		self.interval = interval
		self.action = action

	def set_action(self, action):
		"""
		Sets the action to be performed for an instance of this class

		Keyword arguments:
		action -- the function to call on the timer.
		"""
		self.action = action

	def set_interval(self, interval):
		"""
		Sets the interval to repeat for an instance of this class

		Keyword arguments:
		interval -- the interval at which the timer will sleep before next action
		"""
		self.interval = interval

	def get_runtime():
		"""
		Returns the current runtime of the timer object
		"""
		return time.monotonic - start_time

	def update(self):
		"""
		Updates the timer to perform a set action during a set interval
		"""
		self.next_update += self.interval

		if self.action is None:
			raise ValueError("No action was provided")
		else:
			self.action()

		sleep_time = self.next_update - time.monotonic()
		if sleep_time > 0:
			time.sleep(sleep_time)
