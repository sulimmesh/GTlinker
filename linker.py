import sys
import yaml
import requests

from apscheduler.schedulers.blocking import BlockingScheduler

def link():
	pass

def main(argv):
	if len(argv) > 1:
		#initialize some variables
	scheduler = BlockingScheduler()
	scheduler.add_job(link, "interval", hours=24, id="link_job")

if __name__ == "__main__":
	main(sys.argv[1:])
