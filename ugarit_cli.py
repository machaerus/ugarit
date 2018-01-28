#!/usr/bin/env python

from habanero import Crossref, cn
from scihub import SciHub
import requests
import json
import re


class Ugarit():

	def __init__(self):

		# constants
		self.RES_LIMIT = 3
		self.scopus_url = "http://api.elsevier.com/content/search/scopus"
		self.scopus_key = '23096dfc3e1a8d87504a227fb4314c9f'
		self.scopus_view = "STANDARD"

		# init
		self.sh = SciHub()
		self.cr = Crossref()

	def scopus_submit(self, author, phrase):
		query = re.sub("\s+", "\+", phrase)
		if author != "":
			author = "AUTH%28{}%29".format(re.sub("\s+", "\+", author))
			query = "{}+{}".format(author, query)
		r = requests.get("{}?query={}&apiKey={}&view={}&count={}".format(
				self.scopus_url, 
				query, 
				self.scopus_key, 
				self.scopus_view, 
				self.RES_LIMIT
		))
		self.scopus_res = r.json()
		self.scopus_res = self.scopus_res['search-results']['entry']
		return self.scopus_res

		#data = scopus_submit(author, phrase)
		#doi = data['search-results']['entry'][6]['prism:doi']

	def set_doi(self, doi):
		self.doi = doi

	def get_doi(self, n):
		self.doi = self.scopus_res[n]['prism:doi']
		return self.doi

	def print_scopus_results(self):
		print("Number of articles found: {}".format(len(self.scopus_res)))
		print()
		for article in self.scopus_res:

			title = article['dc:title']
			if len(title) > 50:
				title = title[:50] + " . . ."

			print("[#{}]".format(self.scopus_res.index(article)))
			print(" |    {:30}{}".format("Title:",					title))
			print(" |    {:30}{}".format("Author:",					article['dc:creator']))
			print(" |    {:30}{}".format("Date:",					article['prism:coverDisplayDate']))
			print(" |    {:30}{}".format("Publication name:",		article['prism:publicationName']))
			print(" |    {:30}{}".format("Type:",					article['subtypeDescription']))
			print()


	def unpaywall_check(self, doi):
		r = requests.get("https://api.oadoi.org/v2/{}?email=test@example.com".format(doi))
		response = r.json()
		return response['is_oa']
	
	def unpaywall_download(self, doi, save="test.pdf"):
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

	def crossref_get(self, doi):
		return cn.content_negotiation(ids=doi, format="bibentry")



ugarit = Ugarit()

print()
print("Search for a new article.")
print("-------------------------")
print()

author = input("{:20}".format("Author (optional):"))
keyphrase = input("{:20}".format("Query (mandatory):"))

print()

ugarit.scopus_submit(author, keyphrase)
ugarit.print_scopus_results()

print()

article_no = input("Select article (0-{}): ".format(ugarit.RES_LIMIT-1))
doi = ugarit.get_doi(int(article_no))

print()
print("Checking Unpaywall...")
check_unpaywall = ugarit.unpaywall_check(doi)
if check_unpaywall:
	input = input("Article found on Unpaywall. Do you want to download? [y/n] ")
	if input == "y":
		print("Downloading...")
		ugarit.unpaywall_download(doi)
		print("Done!")
	elif input == "n":
		print("Kthxbai!")
else:
	input = input("Article is not accessible for free. Do you want to try SciHub? [y/n] ")
	if input == "y":
		print("Downloading...")
		if ugarit.scihub_download(doi):
			print("Done!")
		else: 
			print("Sorry, can't find it!")
	elif input == "n":
		print("Kthxbai!")