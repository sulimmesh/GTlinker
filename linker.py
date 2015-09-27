import sys
import yaml
import requests
import logging
#disabling insecureplatformwarnings for cleaner output
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from apscheduler.schedulers.blocking import BlockingScheduler
from git import Git
from trello import Trello
logging.basicConfig()

GIT = "Github Issue"
BUG = "Bug"
ENH = "Enhancement"
QA = "Quality"

def sync(issue, card, younger):
	pass

def link():
	config_yaml = open("config.yaml", "r")
	config = yaml.load(config_yaml)
	trello_board = config["trello_board"]
	git = Git(config["git_username"], config["git_email"], config["git_password"])
	trello = Trello(config["trello_key"], config["trello_token"])
	#first get all issues from the github repo
	shared_topics = {}
	issues = git.getIssues("Brewmaster")
	issue_titles = []
	for issue in issues:
		issue_titles.append(issue["title"])
	#get all cards from trello board
	card_names = []
	cards = trello.getCards(trello_board)
	for card in cards:
		card_names.append(card["name"])
		for label in card["labels"]:
			if github_label == label["name"]:
				if not card["name"] in issue_titles:
					pass
					#add card as a github issue
					#add all comments as github issue comments
				else:
					#add this to the shared_topic with name as the key
					shared_topics[card["name"]] = [card]
	for issue in issues:
		if not issue["title"] in card_names:
			pass
			#add issue as a trello card
			#add all comments as trello card comments
		else:
			#append this issue to the shared_topics with name as the key
			shared_topics[title].append(issue)
	"""
	next check if each issue/card in the dictionary are synced
	if not, then adjust the older version to match the most recently
	updated version
	Check update times:
	card["dateLastActivity"], issue["updated_at"]
	Formatted:
	2015-09-27T00:12:32.556Z 2015-09-26T21:52:01Z
	"""


def main(argv):
	if len(argv) > 1:
		#initialize some variables
		pass
	link()
	#scheduler = BlockingScheduler()
	#scheduler.add_job(link, "cron", minute=58, second=0, id="link_job")
	#scheduler.start()

if __name__ == "__main__":
	main(sys.argv[1:])
