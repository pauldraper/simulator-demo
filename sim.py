import sched

class Scheduler:
	"""Schedules events for the simulator."""

	def __init__(self):
		"""Create an empty scheduler."""
		self.__current = 0
		self.__scheduler = sched.scheduler(self.get_time, self.advance_time)
	
	def get_time(self):
		"""Return current time of Scheduler."""
		return self.__current

	def advance_time(self, units):
		"""Advance time in the Scheduler by the given number of units."""
		self.__current += units

	def add(self, handler, args=(), delay=0, priority=1):
		"""Schedule a function call."""
		return self.__scheduler.enter(delay, priority, handler, args)

	def run(self):
		"""Run scheduled events."""
		self.__scheduler.run()

class TimeoutException(Exception):
	"""Thrown when timeout is needed."""
	def __init__(self, timeout):
		self.timeout = timeout	
def sleep(timeout):
	"""Sleep for timeout."""
	raise TimeoutException(timeout)
	return #In Python 3.3, simply use `yield from iter(())`
	yield

class WaitException(Exception):
	"""Thrown when wait is needed."""
	def __init__(self, lock):
		self.lock = lock
def wait(lock):
	raise WaitException(lock)
	return #In Python 3.3, simply use `yield from iter(())`
	yield
	
class ResumeException(Exception):
	"""Thrown when wait is needed."""
	def __init__(self, lock):
		self.lock = lock
def resume(lock):
	raise ResumeException(lock)
	return #In Python 3.3, simply use `yield from iter(())`
	yield

def create_lock():
	return []

class Simulator:
	"""Controls function calls and flow."""

	def __init__(self):
		"""Creates a new Simulator."""
		self.scheduler = Scheduler()
	
	def new_thread(self, gen):
		"""Add a new thread."""
		self.__proceed([gen])
		
	def run(self):
		"""Run the simulator to completion."""
		self.scheduler.run()
	
	def __proceed(self, stack, args=None):
		"""Perform next call."""
		if not stack:
			return
		try:
			next_call = stack[-1].send(args)
		except StopIteration as e:
			stack.pop()
			self.__proceed(stack, e.args)
		except TimeoutException as e:
			self.scheduler.add(self.__proceed, (stack,), e.timeout)
		except WaitException as e:
			e.lock.append(stack)
		except ResumeException as e:
			stacks, e.lock = e.lock, []
			for stack in stacks:
				self.__proceed(stack)
		else:
			stack.append(next_call)
			self.__proceed(stack)

simulator = Simulator() #singleton

class Logger:
	"""Logs messages (simpler than the built-in logger)."""

	def __init__(self, time_function):
		"""Creates a new logger."""
		self.time_function = time_function
		self.level = 1

	def log(self, text, level=1):
		"""Log a message with the given level."""
		if level <= self.level:
			print '{:10.4f} {}'.format(self.time_function(), text)

logger = Logger(simulator.scheduler.get_time) #singleton
