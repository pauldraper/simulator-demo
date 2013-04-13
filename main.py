from __future__ import division
import string
import random

from host import Host
from link import Packet, Link
from sim import simulator, sleep, logger

class RandomSender:
	"""A client for sending randomly generated messages."""

	def __init__(self, host, dest, message_len, rate):
		"""Creates a RandomSender."""
		self.host = host
		self.dest = dest
		self.message_len = message_len
		self.rate = rate
		
	def send(self, duration):
		"""Sends random messages for specified duration."""
		stop_time = simulator.scheduler.get_time() + duration
		while stop_time > simulator.scheduler.get_time():
			message = ''.join(random.choice(string.letters) for _ in xrange(self.message_len))
			self.host.send(Packet(self.host.ip, self.dest, message))
			yield sleep(random.expovariate(self.rate))


if __name__ == '__main__':
	"""Main method."""
	# set up network
	host1 = Host('123.0.0.0')
	host2 = Host('101.0.0.0')
	link1 = Link(host1, host2, prop_delay=0.5, bandwidth=1000)
	link2 = Link(host2, host1, prop_delay=0.5, bandwidth=1000)

	# set up usage
	mlen = 128
	usage = .90
	rs1 = RandomSender(host1, host2.ip, message_len=mlen, rate=usage*link1.bandwidth/mlen)
	rs2 = RandomSender(host2, host1.ip, message_len=mlen, rate=usage*link1.bandwidth/mlen)
	
	# run
	simulator.new_thread(rs1.send(duration=10))
	simulator.new_thread(rs2.send(duration=10))
	logger.level = 4
	simulator.run()
