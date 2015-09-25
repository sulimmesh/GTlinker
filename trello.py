import requests

class Trello(object):
	def __init__(self, email, password):
		self._email = email
		self._password = password
		self.base_url = "https://api.trello.com/1/"

	def getCards(self, board):
		url = self.base_url+"boards/"+board+"/cards"
		request = requests.get(url, auth=(self._email, self._password))
		return request.json()

	def getCard(self, card):
		url = self.base_url+"/cards/"+card
		request = requests.get(url, auth=(self._email, self._password))
		return request.json()

