import sys
import yaml
import requests
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from git import Git
from trello import Trello
logging.basicConfig()

def link():
	config_yaml = open("config.yaml", "r")
	config = yaml.load(config_yaml)
	trello_board = config["trello_board"]
	git = Git(config["git_username"], config["git_email"], config["git_password"])
	trello = Trello(config["trello_key"], config["trello_token"])
	#first get all issues from the github repo
	issues = git.getIssues("Brewmaster")
	#get all cards from trello board
	cards = trello.getCards(trello_board)
	#getting comments from the first card
	comments = trello.getCardComments(cards[0]["id"])


def main(argv):
	if len(argv) > 1:
		#initialize some variables
		pass

	scheduler = BlockingScheduler()
	scheduler.add_job(link, "cron", minute=41, id="link_job")
	scheduler.start()

if __name__ == "__main__":
	main(sys.argv[1:])
