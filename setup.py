from setuptools import setup, find_packages
from txwhois import version

setup(
	name='txwhois',
	packages=find_packages(),
	version=version,

	install_requires=[
		'twisted',
		'tldextract'
	],

	author='systocrat',
	author_email='systocrat@outlook.com',
	description='Twisted Whois client',
	license='MIT',

	package_data={
		'txwhois': ['resources/tlds.txt']
	}
)