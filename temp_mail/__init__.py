import requests
from bs4 import BeautifulSoup
import re
import time
import _thread

class Client():
	base = "https://temp-mail.org/en"
	def __init__(self, address: str = None):
		self.address = address
		self.session = requests.Session()

		realisticBrowser = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
		}

		if self.address != None:
			self.session.cookies.set("mail", self.address.replace("@", "%40"))

		self.session.headers.update(realisticBrowser)
		self.session.get(self.base)
		try:
			self.address = self.session.cookies["mail"].replace("%40", "@")
		except:
			raise ValueError("The email address you supplied is not supported on temp-mail")
		
		self.recent = []

	def checkloop(self, callback=lambda m: m, async=True):
		if async == True:
			_thread.start_new_thread(self.checkloop(callback=callback, async=False))
		else:
			self.check()
			time.sleep(2)
			while True:
				ilen = len(self.recent)
				self.check()
				if len(self.recent) > ilen:
					for i in self.recent[ilen:]:
						callback(i)
				time.sleep(10)

	def check(self):
		r = self.session.get(self.base + "/option/refresh/")
		soup = BeautifulSoup(r.text, "html.parser")

		mails = []

		for mail in soup.find('tbody').findChildren("tr"):
			info = mail.findChildren("td")[0].findChildren()[0]
			
			view_url = info["href"]
			subject = info["title"]
			by = re.findall(r".*&lt;(.+)&gt;", info.decode_contents())

			creq = self.session.get(view_url)
			contentsoup = BeautifulSoup(creq.text, "html.parser")
			content = contentsoup.find("div", {"class":"pm-text"}).decode_contents()

			themail = Email(author=by, content=content,to=self.address,subject=subject)
			
			mails.append(themail)

		self.recent = mails
		return mails

class Email():
	def __init__(self, author=None, content=None, to=None, subject=None):
		self.author = author
		self.content = content
		self.to = to
		self.subject = subject
	
	def __str__(self):
		return str({"author":self.author, "content": self.content, "to": self.to, "subject":self.subject})

	def links(self):
		soup = BeautifulSoup(self.content, "html.parser")
		lnks = []
		for link in soup.findAll("a"):
			lnks.append(link["href"])
		return lnks