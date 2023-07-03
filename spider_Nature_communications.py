import requests
from bs4 import BeautifulSoup
import re
import random,time


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


def get_latest_issue_inf(paper_url_list, paper_title_list, paper_abstract_list, paper_publishedtime_list, page):
    url = ("https://www.nature.com/ncomms/articles?searchType=journalSearch&sort=PubDate&page=" + str(page))
    print(url)
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    # print(soup)
    each_paper_url = soup.findAll("article")
    # print(each_paper_url)
    # print(len(each_paper_url))
    pattern1 = r'.*href="(.*)" itemprop="url">.*'
    pattern2 = r'.*        (.*)</a>.*'
    pattern4 = r'.*<p>(.*)</p>.*'
    pattern5 = r'.*itemprop="datePublished">(.*)</time>.*'

    for paper in each_paper_url:
        #print(paper)
        paper_url_list.append("https://www.nature.com" + str(
            str(re.findall(pattern1, str(paper.findAll({"a": "href"})))).replace("[", "").replace("]", "").replace("'", "")))
        paper_title_list.append(
            str(re.findall(pattern2, str(paper.findAll({"a": "href"})))).replace("['", "").replace("']", "").replace("'", ""))
        paper_abstract_list.append(
            str(re.findall(pattern4, str(paper.findAll("div", {'itemprop': "description"})))).replace("['", "").replace("']", "").replace("'",
                                                                                                                    ""))
        paper_publishedtime_list.append(
            str(re.findall(pattern5, str(paper.findAll({"time"})))).replace("['", "").replace("']", "").replace("'", ""))
    #print(paper_url_list)
    #print(len(paper_url_list))
    #print(paper_title_list)
    #print(len(paper_title_list))
    #print(paper_abstract_list)
    #print(len(paper_abstract_list))
    print(paper_publishedtime_list)
    return paper_url_list, paper_title_list, paper_abstract_list, paper_publishedtime_list


def Judgement_update(paper_url_list, paper_title_list, paper_abstract_list, paper_publishedtime_list,ISS):
    paper_url = []
    paper_title = []
    paper_abstract = []
    paper_publishedtime = []
    for i in range(0, len(paper_publishedtime_list)):
        #print(paper_publishedtime_list[i])
        if paper_publishedtime_list[i] == ISS:
            if (len(paper_publishedtime)) == 0:
                paper_url.append("null")
                paper_title.append("null")
                paper_abstract.append("null")
                paper_publishedtime.append("ISS")
            return paper_url, paper_title, paper_abstract, paper_publishedtime, int(100)
        else:
            #print(paper_url_list[i])
            paper_url.append(paper_url_list[i])
            paper_title.append(paper_title_list[i])
            paper_abstract.append(paper_abstract_list[i])
            paper_publishedtime.append(paper_publishedtime_list[i])
    return paper_url, paper_title, paper_abstract, paper_publishedtime, int(1)



def spider_Nature_communications(ISS):
    paper_url_list = []
    paper_title_list = []
    paper_abstract_list = []
    paper_publishedtime_list = []
    for page in range(1, 100):
        [paper_url_list, paper_title_list, paper_abstract_list, paper_publishedtime_list] = get_latest_issue_inf(paper_url_list, paper_title_list, paper_abstract_list, paper_publishedtime_list, page)
        [paper_url_list, paper_title_list, paper_abstract_list, paper_publishedtime_list, k] = Judgement_update(paper_url_list, paper_title_list, paper_abstract_list, paper_publishedtime_list, ISS)
        print(k)
        #print(paper_url_list)
        #print(paper_title_list)
        print(paper_publishedtime_list)
        if k == 100:
            #print(paper_title_list)
            #print(paper_url_list)
            #print(paper_publishedtime_list)
            return paper_title_list, paper_url_list, paper_abstract_list, paper_publishedtime_list[0]

    return paper_title_list, paper_url_list, paper_abstract_list, paper_publishedtime_list[0]


#ISS = '23 December 2020'
#print(ISS)
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_Nature_communications(ISS)
#print(len(paper_title_list))
#print(len(paper_url_list))
#print(len(paper_abstract_list))

