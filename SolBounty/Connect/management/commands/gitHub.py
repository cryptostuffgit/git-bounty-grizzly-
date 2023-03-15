from github import Github
from django.core.management.base import BaseCommand, CommandError
import requests
import json
from Connect.models import *
from decimal import Decimal
from datetime import datetime

class Command(BaseCommand):
	help = 'Command to trigger a race to end and create a new one.'

	def handle(self, *args, **options):
		# print('hello')
		# g = Github("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")

		# # Then play with your Github objects:
		# for repo in g.get_user().get_repos():
		# 	if repo.name == "sol_lottery":
		# 		print(repo.name)
		# 		open_issues = repo.get_issues(state='open')
		# 		print("Listing Current Issues:")
		# 		for issue in open_issues:
		# 			print(issue)
		# 		print("Done Current Issues.")
		# 		print("---")
		# 		if input("Created Issue? (y/n)").lower() == "y":
		# 			title = input("Enter Issue Title: ")
		# 			body = input("Enter Issue Body: ")
		# 			issue = repo.create_issue(title=title, body=body)
		# 			print("Created",issue)

		webhook = GitWebhook.objects.get(pk=20)
		data = webhook.data
		try:
			issue = GitIssue.objects.get(github_id=data['ref'].split('-')[-1])
			user = User.objects.get(username=data['commits'][0]['author']['name'])
			print(issue,"Solved by",user)
			BountyPayment.objects.create(
				user=user,
				issue=issue
			)
		except:
			pass
		# print(webhook.data)