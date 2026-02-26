"""
test_timer.py

This module tests the RepeatingTimer class
and ensures input is valid and that its methods
are providing expected output
"""
import pytest
from led.timer import RepeatingTimer


@pytest.mark.parametrize("valid_time", [
	(1),
	(10),
	(100),
	(1000),
	(10000)
])
def test_timer_invalid_intervals(valid_time):
	"""
	Tests invalid intervals of time to ensure they throw an ValueError
	"""
	t = RepeatingTimer(interval=valid_time)

	assert t.get_interval == valid_time


@pytest.mark.parametrize("invalid_time, exception", [
	("a", TypeError),
	("1", TypeError),
	(0, ValueError),
	(-1, ValueError),
	(-1000, ValueError),
])
def test_timer_invalid_intervals(invalid_time, exception):
	"""
	Tests invalid intervals of time to ensure they throw an ValueError
	"""
	t = RepeatingTimer()

	with pytest.raises(exception):
		t.set_interval(invalid_time)

@pytest.mark.parametrize("invalid_action", [
	(None),
	("a"),
	(1),
	(False)
])
def test_timer_invalid_actions(invalid_action):
	"""
	Tests that invalid actions throw an exception
	"""
	t = RepeatingTimer()

	with pytest.raises(TypeError):
		t.set_action(invalid_action)


def test_timer_update_no_action():
	"""
	Tests that a timer with no action throws a runtime exception if updated
	"""
	t = RepeatingTimer()

	with pytest.raises(RuntimeError):
		t.update()
