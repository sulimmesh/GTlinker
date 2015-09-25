import requests

class Trello(object):
	def __init__(self, email, password):
		self._email = email
		self._password = password