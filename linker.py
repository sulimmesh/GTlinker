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
	if len(issue["body"]) > 0:
		created = issue["created_at"]
		created = datetime.strptime(created,"%Y-%m-%dT%H:%M:%SZ")
		issue_comments_list.append([issue["body"], created])
	issue_comments = git.getIssueComments("Brewmaster", str(issue["number"]))
	issue_events = git.getIssueEvents("Brewmaster", str(issue["number"]))
	for event in issue_events:
		time = event["created_at"]
		time = datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
		text = ""
		if event["event"] == "referenced":
			commit = event["commit_id"]
			text += "referenced in "+commit[:6]+"... on "+str(time.date())+"\n"
			commit = git.getCommit("Brewmaster", commit)
			text += commit["commit"]["message"]+" - "+commit["commit"]["committer"]["name"]
			issue_comments_list.append([text,time])
		elif event["event"] == "assigned":
			assignee = event["assignee"]["login"]
			name = None
			for item in config["git_to_trello"]:
				if assignee in item.keys():
					name = item[assignee]
			text = ""
			text += "Assign to "+name+" on "+str(time.date())
			issue_comments_list.append([text,time])
		elif event["event"] == "unassigned":
			assignee = event["assignee"]["login"]
			name = None
			for item in config["git_to_trello"]:
				if assignee in item.keys():
					name = item[assignee]
			text = ""
			text += "Unassign to "+name+" on "+str(time.date())
			issue_comments_list.append([text,time])

	for comment in issue_comments:
		text = comment["body"]
		time = comment["updated_at"]
		time = datetime.strptime(time,"%Y-%m-%dT%H:%M:%SZ")
		issue_comments_list.append([text,date])

	issue_comments_list.sort(key = lambda row: row[1])

	card_comments_list = []
	card_comments = trello.getCardComments(card["id"])
	for comment in card_comments:
		text = comment["data"]["text"]
		time = comment["date"]
		time = datetime.strptime(time,"%Y-%m-%dT%H:%M:%S.%fZ")
		card_comments_list.append([text,time])

	card_comments_list.sort(key = lambda row: row[1])

	for item in issue_comments_list:
		if len(card_comments_list) > 0:
			new_list = []
			for comment in card_comments_list:
				new_list.append(comment[0])
			if not item[0] in new_list:
				trello.comment(card["id"], item[0])
		else:
			trello.comment(card["id"], item[0])

	for item in card_comments_list:
		if len(issue_comments_list) > 0:
			new_list = []
			for comment in issue_comments_list:
				new_list.append(comment[0])
			if not item[0] in new_list:
				response = git.comment("Brewmaster", str(issue["number"]), item[0])
		else:
			git.comment("Brewmaster", str(issue["number"]), item[0])

	lists = trello.getLists(config["trello_board"])
	labels = trello.getLabels(config["trello_board"])
	if newer == "issue":
		list_id = None
		status = issue["state"]
		if status == "open":
			target_list = None
			if len(issue_comments)+len(issue_events) > 0:
				target_list = "To Do"
			else:
				target_list = "Doing"
			for list in lists:
				if list["name"] == target_list:
					list_id = list["id"]
		if status == "closed":
			target_list = "closed"
			for list in lists:
				if list["name"] == target_list:
					list_id = list["id"]
		trello.moveCard(card["id"], list_id)

		issue_labels = issue["labels"]
		issue_names = []
		for label in issue_labels:
			issue_names.append(label["name"])
		for label in labels:
			if label["name"].lower() in issue_names:
				trello.addLabel(card["id"], label["id"])
			if label["name"] == GIT:
				trello.addLabel(card["id"], label["id"])
	elif newer == "card":
		new_state = None
		status = card["idList"]
		for list_id in lists:
			if list_id["id"] == status:
				status = list_id["name"]
		if status == "Done":
			new_state = "closed"
		else:
			new_state = "open"

		label_names = []
		for label in card["labels"]:
			label_names.append(label["name"])
		git.updateIssue("Brewmaster", str(issue["number"]), labels=label_names, 
			state=new_state)

def link():
	config_yaml = open("config.yaml", "r")
	config = yaml.load(config_yaml)
	config_yaml.close()
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
					label_list = []
					for label in card["labels"]:
						if not label["name"] == GIT:
							label_list.append(label["name"])
					title = card["name"]
					body = card["desc"]
					response = git.raiseIssue("Brewmaster", title, body, 
						labels=label_list)
					comments = trello.getCardComments(card["id"])
					for comment in comments:
						body = comment["data"]["text"]
						git.comment("Brewmaster", response["number"],
							body)	
				else:
					shared_topics[str(card["name"])] = [card]

	lists = trello.getLists(config["trello_board"])
	labels = trello.getLabels(config["trello_board"])
	for issue in issues:
		if not issue["title"] in card_names:
			#add issue as a trello card
			#label it
			name = issue["title"]
			desc = issue["body"]
			label_list = []
			for label in issue["labels"]:
				label_list.append(label["name"])
			label_ids = []
			for label in labels:
				if label["name"].lower() in label_list:
					label_ids.append(label["id"])
				if label["name"] == GIT:
					label_ids.append(label["id"])
			list_name = None
			if issue["state"] == "open":
				if issue["comments"] > 0:
					list_name = "Doing"
				else:
					list_name = "To Do"
			else:
				list_name = "Done"
			list_id = None
			for list in lists:
				if list["name"] == list_name:
					list_id = list["id"]
			response = trello.addCard(name, desc, list_id, label_ids)
			#add all comments as trello card comments
			comments = git.getIssueComments("Brewmaster", str(issue["number"]))
			for comment in comments:
				body = comment["body"]
				trello.comment(response["id"], body)
		else:
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
	scheduler = BlockingScheduler()
	scheduler.add_job(link, "interval", hours=1, id="link_job")
	scheduler.start()

if __name__ == "__main__":
	main(sys.argv[1:])
