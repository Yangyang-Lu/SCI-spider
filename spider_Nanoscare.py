import requests
import json
url = "https://pubs.rsc.org/en/journals/journalissues/nr?&_ga=2.268503154.2045026669.1607676163-1226190415.1586434805#!issueid=nr012046&type=current&issnprint=2040-3364"
r = requests.request("post", url)
print(r.text)
d = json.load(r.text)
print(d['issue-navigator'])
