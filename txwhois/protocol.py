from twisted.internet.defer import Deferred
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver


class WhoisClientProtocol(LineReceiver):
	delimiter = b'\n'

	def __init__(self, factory):
		self.factory = factory
		self.headers = {}
		self.whois = []

	def connectionMade(self):
		domain = '%s\r\n' % (self.factory.domain,)
		self.transport.write(domain.encode('utf-8'))

	def lineReceived(self, line):
		line = line.decode('utf-8')

		parts = line.split(':', 1)

		# Okay, so header lines are delimited by \n
		# Non-header lines (ie the actual whois info) are delimited by \r\n
		# this is why this check exists

		if len(parts) > 1 and not line.endswith('\r'):
			header_name = parts[0].strip().lower()
			header_value = parts[1].strip()
			self.headers[header_name] = header_value
		else:
			self.whois.append(line.strip())

	def connectionLost(self, reason):
		self.factory.finished.callback((self.headers, self.whois))


class WhoisClientFactory(Factory):
	def __init__(self, domain):
		self.domain = domain
		self.finished = Deferred()

	def buildProtocol(self, addr):
		return WhoisClientProtocol(self)
