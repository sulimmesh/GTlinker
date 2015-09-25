import sys
import yaml
import requests

from apscheduler.schedulers.blocking import BlockingScheduler

class Git(object):
	def __init__(self, username, email, password):
		self._username = username
		self._email = email
		self._password = password
		self.base_url = "https://api.github.com/"

	def getIssues(self, repo):
		url = self.base_url+"repos/"+self._username+"/"+repo+"/issues"
		request = requests.get(url, auth=(self._username, self._password))
		issues = request.json()
		return issues

class Trello(object):
	def __init__(self, email, password):
		self._email = email
		self._password = password

def link():
	config_yaml = open("config.yaml", "r")
	config = yaml.load(config_yaml)
	git = Git(config["git_username"], config["git_email"], config["git_password"])
	trello = Trello(config["trello_email"], config["trello_password"])
	issues = git.getIssues("Brewmaster")

def main(argv):
	if len(argv) > 1:
		#initialize some variables
		pass
	scheduler = BlockingScheduler()
	scheduler.add_job(link, "cron", minute=18, id="link_job")
	scheduler.start()


if __name__ == "__main__":
	main(sys.argv[1:])
