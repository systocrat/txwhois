import attr
import json
import sys
from attr import Factory
from attr.validators import instance_of


@attr.s
class WhoisServerCache(object):
	# dictionary of
	# {
	#     (tld, True): server,
	#     (server, False): tld
	# }

	servers = attr.ib(Factory(dict), validator=instance_of(dict))

	def server_for_tld(self, tld):
		return self.servers[(tld, True)]

	def tld_for_server(self, server):
		return self.servers[(server, False)]

	def set_tld_server(self, tld, server):
		self.servers[(tld, True)] = server
		self.servers[(server, False)] = tld

	def to_dictionary(self):
		if sys.version_info[0] < 3:
			keyiter = 'iterkeys'
		else:
			keyiter = 'keys'

		result = {}

		for (item, istld) in getattr(self.servers, keyiter)():
			if istld:
				result[item] = self.server[(item, istld)]

		return result

	@staticmethod
	def from_dictionary(json_object):
		if sys.version_info[0] < 3:
			keyiter = 'iterkeys'
		else:
			keyiter = 'keys'

		servers = {}
		for tld in getattr(json_object, keyiter)():
			server = json_object[tld]

			servers[(tld, True)] = server
			servers[(server, False)] = tld

		return WhoisServerCache(servers=servers)
