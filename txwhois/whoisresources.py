import os

# resource folder (txwhois/resources)
resource_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources'))

# list of tlds, published by iana at https://data.iana.org/TLD/tlds-alpha-by-domain.txt
tld_file_path = os.path.join(resource_folder_path, 'tlds.txt')


def load_tlds():
	tlds = list()

	with open(tld_file_path, 'r') as f:
		for line in f:
			line = line.strip()

			if '#' in line:
				continue

			tlds.append(line)

	# we return a set because we assume that people will want to check if a tld exists
	# in O(1) time
	return set(tlds)
