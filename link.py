from __future__ import division
from collections import deque
import itertools

from sim import logger, sleep, simulator

log = lambda x: logger.log(x, 4) #link layer

class Packet:
	"""Represents a network packet."""
	id_counter = itertools.count()

	def __init__(self, origin, dest, message):
		self.id = Link.id_counter.next()
		self.origin = origin
		self.dest = dest
		self.message = message

	@property
	def size(self):
		return (len(self.message) if self.message else 0) + 4

class Link:
	"""Represents a unidirectional link."""
	id_counter = itertools.count()

	def __init__(self, source, dest, prop_delay, bandwidth):
		"""Creates a Link between the specified Hosts, with the given performance.
		(This also adds the Link to the source Host's outgoing links.)"""
		self.id = Link.id_counter.next()
		self.dest = dest
		self.prop_delay = prop_delay
		self.bandwidth = bandwidth
		self.busy = False
		self.queue = deque()
		source.routing[dest.ip] = self

	#non-blocking
	def enqueue(self, packet):
		"""Called to place this packet in the queue."""
		log('queue-start %d %d' % (self.id, packet.id))
		self.queue.appendleft(packet)
		if not self.busy:
			simulator.new_thread(self.__transmit())

	def __transmit(self):
		"""Transmit packet."""
		packet = self.queue.pop()
		log('queue-end %d %d' % (self.id, packet.id))
		
		log('transmit-start %d %d' % (self.id, packet.id))
		self.busy = True
		yield sleep(packet.size / self.bandwidth)
		log('transmit-end %d %d' % (self.id, packet.id))
		
		self.busy = False
		if self.queue:
			simulator.new_thread(self.__transmit())
		
		log('propogate-start %d %d' % (self.id, packet.id))
		yield sleep(self.prop_delay)
		log('propogate-end %d %d' % (self.id, packet.id))
		
		yield self.dest.received(packet)
