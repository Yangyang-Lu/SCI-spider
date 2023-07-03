import requests
from bs4 import BeautifulSoup
import re
import random,time
from compare_url_title import compare_url_title

def get_content(url):
    headers = {
        "referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36"}
    try_number = 0
    while try_number < 10:
        try:
            content = requests.get(url, headers=headers, timeout=120)
            content.encoding = "utf-8"
            # print(content.text)
            time.sleep(random.randint(0, 5))
            return content.text
        except requests.exceptions.RequestException:
            try_number += 1
            content = []
            print("time out")
    if content == []:
        content = requests.get('https://www.google.com/')

    return content.text


def get_page(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("div", {'class': "highwire-cite-highlight"})
    print(each_paper_url)
    print(each_paper_url[len(each_paper_url)-1])
    pattern1 = r'.*href="(.*)"><img alt.*'
    pattern2 = r'\d+'

    url = str(re.findall(pattern1, str(each_paper_url[len(each_paper_url)-1]))).replace("['", "").replace("']", "")
    k = re.findall(pattern2, str(url))
    latest_issue_inf = ("Vol. "+str(k[0])+", Iss. "+str(k[1]))
    latest_issue_url = ("https://science.sciencemag.org"+str(url))
    #print(latest_issue_url)
    #print(latest_issue_inf)
    return latest_issue_inf, latest_issue_url


def get_latest_issue_inf(url):
    content = get_content(url)
    #print(content)
    soup = BeautifulSoup(content, 'html.parser')
    #print(soup)
    each_paper_url = soup.findAll("h3", {'class': "highwire-cite-title-wrapper media__headline"})
    #each_paper_url = soup.findAll("div")
    #print(each_paper_url)
    #print(len(each_paper_url))
    pattern1 = r'.*href="(.*?)"><div class=".*'
    pattern2 = r'.*headline__title">(.*)</div></a></h3>.*'
    paper_url_list = []
    paper_title_list = []
    for paper in each_paper_url:
        #print(paper)
        #paper_url_list.append("https://pubs.acs.org/"+str(paper_url.replace('full', 'abs')))
        paper_url_list.append("https://science.sciencemag.org" + str(str(re.findall(pattern1, str(paper))).replace("[", "").replace("]", "").replace("'", "")))
        paper_title_list.append(str(re.findall(pattern2, str(paper))).replace("['", "").replace("']", "").replace("'", ""))
    #print(paper_url_list)
    #print(len(paper_url_list))
    #print(paper_title_list[1])
    #print(len(paper_title_list))
    return paper_url_list, paper_title_list


def get_abstract(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    #each_paper_url = soup.findAll("div", {'class': "section editor-summary"})
    each_paper_url = soup.findAll("div", {'id': "abstract-2"})
    pattern1 = r'.*">(.*)</p>.*'
    #print(1)
    #print(each_paper_url)
    latest_issue_inf = str(re.findall(pattern1, str(each_paper_url))).replace("['", "").replace("']", "").replace('["', '').replace('"]', '')
    return str(latest_issue_inf)

def spider_AAAS_Science(ISS):
    url = ("https://science.sciencemag.org/content/by/year")
    [latest_issue, latest_issue_url] = get_page(url)
    print(latest_issue_url)
    print(latest_issue)
    if latest_issue == ISS:
        url_list = []
        url_list.append(str(latest_issue_url))
        print(url_list)
    else:
        url_list = []
        url_list.append(str(latest_issue_url))
        pattern1 = r'\d+'
        iss = re.findall(pattern1, str(ISS))
        url_list.append("https://science.sciencemag.org/content/" + str(int(iss[0])) + "/" + str(int(iss[1])))
        print(url_list)
    paper_url_list = []
    paper_title_list = []
    for url in url_list:
        [paper_url, paper_title] = get_latest_issue_inf(url)
        for paper_url_1 in paper_url:
            paper_url_list.append(paper_url_1)
        for paper_title_1 in paper_title:
            paper_title_list.append(paper_title_1)
    print(len(paper_url_list))
    [paper_url_list, paper_title_list] = compare_url_title(paper_url_list, paper_title_list, "data\\AAAS_Science.csv", "data\\Temp\\AAAS_Science.csv")
    print(len(paper_url_list))
    if len(paper_url_list) > 0:
        paper_abstract_list = ["a" for _x in range(len(paper_url_list))]
        for i in range(0, len(paper_url_list)):
            print(paper_url_list[i])
            paper_abstract_list[i] = get_abstract(paper_url_list[i])
            # print(paper_abstract_list[i])
        return paper_title_list, paper_url_list, paper_abstract_list, latest_issue
    else:
        paper_title_list = []
        paper_url_list = []
        paper_abstract_list = []
        return paper_title_list, paper_url_list, paper_abstract_list, latest_issue




#ISS = 'Vol. 373, Iss. 6558'
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_AAAS_Science(ISS)
#print(paper_title_list)
#print(paper_url_list)
#print(paper_abstract_list)
#print(len(paper_abstract_list))
#<a class="sans-serif text-reset animation-underline" href="/doi/10.1126/science.abm3757" title="Climate science speaks: “Act now”">Climate science speaks: “Act now”</a>