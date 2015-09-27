import requests
import json

class Git(object):
	def __init__(self, username, email, password):
		self._username = username
		self._email = email
		self._password = password
		self.base_url = "https://api.github.com/"

	def getCommit(self, repo, commit):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/commits/"+commit
		request = requests.get(url, auth=(self._username, self._password))
		commit = request.json()
		return commit		

	def getIssues(self, repo):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues"
		request = requests.get(url, auth=(self._username, self._password))
		issues = request.json()
		return issues

	def getIssue(self, repo, issue):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues/"+issue
		request = requests.get(url, auth=(self._username, self._password))
		issue = request.json()
		return issue

	def raiseIssue(self, repo, title, body, aasignee=None, milestone=None, 
		labels=None):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues"
		payload = {}
		payload["title"] = title
		payload["body"] = body
		if assignee: payload["assignee"] = assignee
		if milestone: payload["milestone"] = milestone
		if labels:
			payload["labels"] = []
			for label in labels:
				payload["labels"].append(label)
		request = requests.post(url, auth=(self._username, self._password),
			data=json.dumps(payload))
		return request.json()

	def updateIssue(self, repo, issue, title=None, body=None, 
		assignee=None, state=None, milestone=None, labels=None):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues/"+issue
		payload = {}
		if title: payload["title"] = title
		if body: payload["body"] = body
		if state: payload["state"] = state
		if assignee: payload["assignee"] = assignee
		if milestone: payload["milestone"] = milestone
		if labels:
			payload["labels"] = []
			for label in labels:
				payload["labels"].append(label)
		request = requests.post(url, auth=(self._username, self._password),
			data=json.dumps(payload))
		return request.json()

	def getIssueComments(self, repo, issue):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues/"+issue+"/comments"
		request = requests.get(url, auth=(self._username, self._password))
		comments = request.json()
		return comments

	def getIssueEvents(self, repo, issue):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues/"+issue+"/events"
		request = requests.get(url, auth=(self._username, self._password))
		events = request.json()
		return events

	def comment(self, repo, issue, body, comment_id=None):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues/"+issue+"/comments"
		if comment_id:
			url += "/"+comment_id
		payload = {}
		payload["body"] = body
		request = requests.post(url, auth=(self._username, self._password), 
			data=json.dumps(payload))
		comment = request.json()
		return comment

	def deleteComment(self, repo, issue, comment_id):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues/"+issue+"/comments/"+comment_id
		request = requests.delete(url, auth=(self._username, self._password))
		status = request.status
		return status

