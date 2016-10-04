try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
	'name':'mets_dnx',
	'version':'0.1.0',
	'author':'Sean Mosely',
	'author_email':'sean.mosely@gmail.com',
	'packages':['mets_dnx',],
	'description':'Python library for building Rosetta DNX/METS XML documents',
	'install_requires':['lxml', 'nose', 'pymets','pydc', 'pydnx']}

setup(**config)