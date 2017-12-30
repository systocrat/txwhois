from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.endpoints import HostnameEndpoint

from .protocol import WhoisClientFactory


class TLDLookupFailed(Exception):
	def __init__(self, headers):
		self.headers = headers


@inlineCallbacks
def lookup_tld_server(tld, whois_server_cache=None, reactor=None):
	"""
	Looks up the whois server for `tld` and returns a Deferred that calls back with
	a unicode string containing the hostname for the whois server for that tld
	"""
	if reactor is None:
		from twisted.internet import reactor

	endpoint = HostnameEndpoint(reactor, 'whois.iana.org', 43)

	factory = WhoisClientFactory(tld)

	yield endpoint.connect(factory)

	headers, _ = yield factory.finished

	try:
		result = headers['whois']

		if whois_server_cache is not None:
			whois_server_cache.set_tld_server(tld, result)

		returnValue(result)
	except KeyError:
		raise TLDLookupFailed(headers)
