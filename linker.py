import sys
import yaml
import requests
import logging
#disabling insecureplatformwarnings for cleaner output
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from git import Git
from trello import Trello
logging.basicConfig()

GIT = "Github Issue"
BUG = "Bug"
ENH = "Enhancement"
QA = "Quality"
Q = "Question"

def sync(git, trello, issue, card, newer, config):
	#first update comments both ways. No comment deletion yet.
	issue_comments_list = []
	issue_comments_list.append(issue["body"])
	issue_comments = git.getIssueComments("Brewmaster", str(issue["number"]))
	issue_events = git.getIssueEvents("Brewmaster", str(issue["number"]))
	for event in issue_events:
		time = event["created_at"]
		time = datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
		text = ""
		if event["event"] == "referenced":
			commit = event["commit_id"]
			text += "referenced in "+commit[:6]+"... on"+str(time.date())+"\n"
			commit = git.getCommit("Brewmaster", commit)
			text += commit["message"]+" - "+commit["author"]["name"]
			issue_comments_list.append([text,time])
		elif event["event"] == "assigned":
			assignee = event["assignee"]["login"]
			name = None
			for item in config["git_to_trello"]:
				if assignee in items.keys():
					name = item[assignee]
			text = ""
			text += "Assign to "+name+" on "+str(time.date())
		elif event["event"] == "unassigned":
			assignee = event["assignee"]["login"]
			name = None
			for item in config["git_to_trello"]:
				if assignee in items.keys():
					name = item[assignee]
			text = ""
			text += "Unassign to "+name+" on "+str(time.date())

	for comment in issue_comments:
		text = comment["body"]
		time = comment["updated_at"]
		time = datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
		issue_comments_list.append([text,date])

	issue_comments_list.sort(key = lambda row: row[1])

	card_comments_list = []
	card_comments = trello.getCardComments(card["id"])
	for comment in card_comments:
		text = comments["data"]["text"]
		time = comments["date"]
		time = datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
		card_comments_list.append([text,time])

	card_comments_list.sort(key = lambda row: row[1])

	for item in issue_comments_list:
		if not item[0] in card_comments_list:
			trello.comment(card["id"], item[0])

	for item in card_comments_list:
		if not item[0] in issue_comments_list:
			git.comment("Brewmaster", issue["number"], item[0])

	if newer == "issue":
		#change position
		#change labels
		pass
	elif newer == "card":
		#change state
		#change labels
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
			if GIT == label["name"]:
				if not card["name"] in issue_titles:
					pass
					#add card as a github issue
					#label it
					#add all comments as github issue comments
				else:
					#add this to the shared_topic with name as the key
					shared_topics[card["name"]] = [card]
	for issue in issues:
		if not issue["title"] in card_names:
			pass
			#add issue as a trello card
			#label it
			#add all comments as trello card comments
		else:
			#append this issue to the shared_topics with name as the key
			shared_topics[issue["title"]].append(issue)

	"""	next check if each issue/card in the dictionary are synced
	if not, then adjust the older version to match the most recently
	updated version
	Check update times:
	card["dateLastActivity"], issue["updated_at"]
	Formatted:
	2015-09-27T00:12:32.556Z 2015-09-26T21:52:01Z """

	for key in shared_topics.keys():
		#both on Zulu time
		issue = shared_topics[key][1]
		card = shared_topics[key][0]
		issue_time = issue["updated_at"]
		card_time = card["dateLastActivity"]
		issue_time = datetime.strptime(issue_time,"%Y-%m-%dT%H:%M:%SZ")
		card_time = datetime.strptime(card_time,"%Y-%m-%dT%H:%M:%S.%fZ")
		if issue_time > card_time:
			sync(git, trello, issue, card, "issue", config)
		elif card_time > issue_time:
			sync(git, trello, issue, card, "card", config)


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
