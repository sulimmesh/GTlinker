import requests

class Trello(object):
	def __init__(self, email, password):
		self._email = email
		self._password = password
		self.base_url = "https://api.trello.com/1/"

	def getBoards(self):
		url = self.base_url+"boards/"
		request = requests.get(url, auth=(self._email, self._password))
		return request.json()

	def getCards(self, board):
		url = self.base_url+"boards/"+board+"/cards"
		request = requests.get(url, auth=(self._email, self._password))
		return request.json()

	def getCard(self, card):
		url = self.base_url+"cards/"+card
		request = requests.get(url, auth=(self._email, self._password))
		return request.json()

	def addCard(self, name, desc, idList, idLabels):
		url = self.base_url+"cards"
		payload = {}
		payload["name"] = name
		payload["desc"] = desc
		payload["idList"] = idList
		payload["idLabels"] = idLabels
		request = requests.post(url, auth=(self._email, self._password),
			data=payload)
		return request.json()

	def moveCard(self, card, list_id):
		url = self.base_url+"cards/"+card+"/idList"
		payload = {}
		payload["value"] = list_id
		request = requests.put(url, auth=(self._email, self._password))
		return request.json()

	def addComment(self, card, body):
		url = self.base_url+"cards/"+card+"/actions/comments"
		payload = {}
		payload["text"] = body
		request = requests.post(url, auth=(self._email, self._password))
		return request.json()
		