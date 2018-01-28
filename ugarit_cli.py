#!/usr/bin/env python

from habanero import Crossref, cn
from scihub import SciHub
import requests
import json
import re

"""

@author: machaerus

TODO:
	- add timeouts
	- implement retries where missing
	- allow to download more than 20 items

"""

class Ugarit():

	def __init__(self):

		# constants
		self.TRIALS = 3

		# init
		self.sh = SciHub()
		self.cr = Crossref()

	def crossref_search(self, query, offset):
		print("Searching...")
		trial = 0
		while trial < self.TRIALS:
			try:
				r = self.cr.works(query=query, offset=offset)
			except Exception:
				print("Error while calling API. Retrying...")
				trial += 1
				time.sleep(1)
				continue
			if r['status'] == "ok":
				results = r['message']['items']
				results = [item for item in results if
								"DOI" in item.keys() and
								"title" in item.keys() and
								"author" in item.keys()]
				if offset == 0:
					self.search_results = results
				else:
					self.search_results += results
				return True
			else:
				print("Incorrect server response. Retrying...")
				trial += 1
				time.sleep(1)
				continue
		print("Search failed. Something's broken.")
		return False

	def set_doi(self, doi):
		self.doi = doi

	def get_doi(self, n):
		self.doi = self.search_results[n]['DOI']
		return self.doi

	def print_search_results(self):
		print("Number of articles found: {}".format(len(self.search_results)))
		print()
		for article in self.search_results:

			title = article['title'][0]
			if len(title) > 60:
				title = title[:60] + " . . ."

			try:
				author = ""
				for a in article['author']:
					author += "{}, {}; ".format(a['family'], a['given'])
				author = author[:-2]
			except Exception as e:
				print(article)
				raise


			if article['issued']['date-parts'][0][0] is not None:	
				date = article['issued']['date-parts'][0][0]
			else:
				date = article['created']['date-parts'][0][0]

			print("[#{}]".format(self.search_results.index(article)))
			print(" |    {:30}{}".format("Title:",					title))
			print(" |    {:30}{}".format("Author:",					author))
			print(" |    {:30}{}".format("Date:",					date))
			print(" |    {:30}{}".format("Publisher:",				article['publisher']))
			print(" |    {:30}{}".format("Type:",					article['type']))
			print()


	def unpaywall_check(self, doi):
		r = requests.get("https://api.oadoi.org/v2/{}?email=test@example.com".format(doi))
		response = r.json()
		return response['is_oa']
	
	def unpaywall_download(self, doi, save="test2.pdf"):
		# https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads
		r = requests.get("https://api.oadoi.org/v2/{}?email=test@example.com".format(doi))
		response = r.json()
		for loc in response['oa_locations']:
			if loc['url_for_pdf']:
				dl = requests.get(loc['url_for_pdf'])
				with open(save, 'wb') as output:
					output.write(dl.content)
				return True
			else:
				continue
		return False

	def scihub_download(self, doi, save="text2.pdf"):
		try:
			dl = self.sh.download(doi)
		except Exception as e:
			print(e)
			return False
		return True

	def crossref_get_citation(self, doi):
		return cn.content_negotiation(ids=doi, format="bibentry")


def main():

	ugarit = Ugarit()

	print()
	print("Search for a new article.")
	print("-------------------------")
	print()

	query = input("{:20}".format("Query:"))

	print()

	offset = 0
	while True:
		ugarit.crossref_search(query, offset)
		ugarit.print_search_results()
		print()
		load_more = input("Load more results? [y/n] ")
		if load_more == "n":
			break
		elif load_more == "y":
			offset += 20
			continue
		break

	print()

	article_no = input("Select article: ")
	doi = ugarit.get_doi(int(article_no))

	print("[1] Download item")
	print("[2] Download citation (BibTeX)")
	action_download = input("What do you want to do? ")

	if action_download == "1":

		print()
		print("Checking Unpaywall...")
		check_unpaywall = ugarit.unpaywall_check(doi)
		if check_unpaywall:
			action = input("Article found on Unpaywall. Do you want to download? [y/n] ")
			if action == "y":
				print("Downloading (a little patience please)...")
				ugarit.unpaywall_download(doi)
				print("Done!")
			elif action == "n":
				print("Kthxbai!")
		else:
			action = input("Article is not accessible for free. Do you want to try SciHub? [y/n] ")
			if action == "y":
				print("Downloading (a little patience please)...")
				if ugarit.scihub_download(doi):
					print("Done!")
				else: 
					print("Sorry, can't find it!")
			elif action == "n":
				print("Kthxbai!")

	elif action_download == "2":

		print()
		print("Downloading citation data...")
		citation = ugarit.crossref_get_citation(doi)
		print()
		print(citation)
		print()


if __name__ == '__main__':
	main()