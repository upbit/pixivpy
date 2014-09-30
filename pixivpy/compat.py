from sys import version_info

py2 = version_info.major < 3

if py2:
	from StringIO import StringIO as BytesIO
	StringIO = BytesIO
	from httplib import HTTPConnection
	from urllib import urlencode
	text = unicode
else:
	from io import BytesIO, StringIO
	from http.client import HTTPConnection
	from urllib.parse import urlencode
	text = str

__all__ = ("py2", "BytesIO", "StringIO", "HTTPConnection", "urlencode", "text")
