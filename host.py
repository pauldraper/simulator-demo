from link import Link
from sim import logger

log = lambda x: logger.log(x, 2) #transport layer

class Host:
	"""Represent a host on the Internet.
	Currently, a host may have exactly one IP address.
	"""

	def __init__(self, ip):
		"""Construct a host with the given ip address."""
		self.ip = ip
		self.routing = {} #ip address to link
		Link(self, self, 0, 100000)

	# data transfer

	#non-blocking
	def send(self, packet):
		"""Send packet."""
		try:
			self.routing[packet.dest].enqueue(packet)
		except KeyError:
			log('{host.ip} has no entry for {packet.dest}', host=self, packet=packet)

	def received(self, packet):
		"""Called (by Link) to deliver a packet to this Host."""
		if packet.dest != self.ip:
			log('{host.ip} received packet for ip {packet.dest}'.format(host=self, packet=packet))
		log('{host.ip} received packet {packet.id}'.format(host=self, packet=packet))
		return
		yield
