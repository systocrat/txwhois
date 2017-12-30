# txwhois
IANA whois library on top of the Twisted networking framework

## Installation

```
git clone https://github.com/systocrat/txwhois
cd txwhois
pip install .
cd .. && rm -rf txwhois
```

## Usage

Create a server cache to store Whois server hostnames for TLDs

```
from txwhois import WhoisServerCache

cache = WhoisServerCache()
```

Then, lookup a domain (assume inlineCallbacks):

```
from txwhois import lookup_domain

all_headers, all_whois_info = yield lookup_domain('google.com', whois_server_cache=cache)
```

`all_headers` is a list of dictionaries containing all headers received by any intermediary whois servers used when
looking up the information for the domain.

`all_whois_info` is a list of lists containing all lines of whois information received by any intermediary whois servers
when looking up the information for the domain.

You can serialize a WhoisServerCache to a dictionary for storage by calling `.to_dictionary` and create a
new WhoisServerCache from storage by calling `.from_dictionary`.
