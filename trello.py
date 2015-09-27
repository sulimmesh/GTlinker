from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
from urllib import urlencode
import requests

class Trello(object):
	def __init__(self, key, token):
		self._auth = {
			"key": key,
			"token": token
		}
		self.base_url = "https://api.trello.com/1/"

	def getLabels(self, board):
		url = self.base_url+"boards/"+board+"/labels"
		url += "?" + urlencode(self._auth)
		request = requests.get(url)
		return request.json()	

	def addLabel(self, card, label):
		url = self.base_url+"cards/"+card+"/idLabels"
		url += "?" + urlencode(self._auth)
		payload = {}
		payload["value"] = label
		request = requests.put(url, data=payload)
		return request.json()


	def getLists(self, board):
		url = self.base_url+"boards/"+board+"/lists"
		url += "?" + urlencode(self._auth)
		request = requests.get(url)
		return request.json()		

	def getCards(self, board):
		url = self.base_url+"boards/"+board+"/cards"
		url += "?" + urlencode(self._auth)
		request = requests.get(url)
		return request.json()

	def getCard(self, card):
		url = self.base_url+"cards/"+card
		url += "?" + urlencode(self._auth)
		request = requests.get(url)
		return request.json()

	def getCardComments(self, card):
		url = self.base_url+"cards/"+card+"/actions"
		url += "?" + urlencode(self._auth)
		request = requests.get(url)
		return request.json()		

	def addCard(self, name, desc, idList, idLabels):
		url = self.base_url+"cards"
		url += "?" + urlencode(self._auth)
		payload = {}
		payload["name"] = name
		payload["desc"] = desc
		payload["idList"] = idList
		payload["idLabels"] = idLabels
		request = requests.post(url,
			data=payload)
		return request.json()

	def moveCard(self, card, list_id):
		url = self.base_url+"cards/"+card+"/idList"
		url += "?" + urlencode(self._auth)
		payload = {}
		payload["value"] = list_id
		request = requests.put(url, data=payload)
		return request.json()

	def comment(self, card, body):
		url = self.base_url+"cards/"+card+"/actions/comments"
		url += "?" + urlencode(self._auth)
		payload = {}
		payload["text"] = body
		request = requests.post(url, data=payload)
		return request.json()


