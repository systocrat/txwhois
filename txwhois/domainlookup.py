import tldextract
from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.internet.endpoints import HostnameEndpoint

from .protocol import WhoisClientFactory
from .tldlookup import lookup_tld_server


@inlineCallbacks
def lookup_domain(domain, whois_server_cache=None, server=None, reactor=None):
	if reactor is None:
		from twisted.internet import reactor

	tldinfo = tldextract.extract(domain)

	if server is None:
		try:
			endpoint = HostnameEndpoint(reactor, whois_server_cache.server_for_tld(tldinfo.suffix), 43)
		except (KeyError, AttributeError) as ex:

			tld_server = yield lookup_tld_server(tldinfo.suffix, whois_server_cache, reactor)
			endpoint = HostnameEndpoint(reactor, tld_server, 43)

	else:
		endpoint = HostnameEndpoint(reactor, server, 43)

	factory = WhoisClientFactory(domain)

	yield endpoint.connect(factory)

	headers, whois = yield factory.finished

	all_headers = [headers]
	all_whois_info = [whois]

	try:
		next_server = headers['whois server']

		more_headers, more_whois_info = yield lookup_domain(domain, server=next_server)

		all_headers.extend(more_headers)
		all_whois_info.extend(more_whois_info)

		returnValue((all_headers, all_whois_info))
	except KeyError:
		returnValue((all_headers, all_whois_info))
