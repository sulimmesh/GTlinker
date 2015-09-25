import sys
import yaml
import requests

from apscheduler.schedulers.blocking import BlockingScheduler
from git import Git
from trello import Trello

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
