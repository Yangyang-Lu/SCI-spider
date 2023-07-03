import requests
from bs4 import BeautifulSoup
import re
import random,time
from compare_url import compare_url

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
    #print(content)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("a", {'class': "visitable"})
    pattern = r'\d+'
    Vol_Iss = re.findall(pattern, str(each_paper_url[0].get('href')))
    k = ("Vol. "+str(Vol_Iss[2])+", Iss. "+str(Vol_Iss[3]))
    url = ("https://www.onlinelibrary.wiley.com" + str(each_paper_url[0].get('href')))
    #print(k)
    #print(url)
    return str(k), str(url)


def get_latest_issue_inf(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("a", {'class': "issue-item__title visitable"})
    paper_url_list = []
    for paper in each_paper_url:
        paper_url = paper.get('href')
        paper_url_list.append("https://www.onlinelibrary.wiley.com" + str(paper_url))
    return paper_url_list


def get_abstract(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    if (len(soup.findAll("meta", {'name': "citation_title"}))) > 0:
        paper_title = soup.findAll("meta", {'name': "citation_title"})[0].get('content')
    else:
        paper_title = []
    each_paper_abstract = soup.findAll("section", {'class': "article-section article-section__abstract"})
    #print(paper_title)
    pattern1 = r'.*<p>(.*)\n.*'
    pattern2 = r'<.*?>'
    paper_abstract = re.sub(pattern2, "", str(re.findall(pattern1, str(each_paper_abstract))), count=0).replace("['", "").replace("']", "")
    return paper_title, paper_abstract


def spider_Wiley_Angew(ISS):
    url = ("https://www.onlinelibrary.wiley.com/loi/15213773")
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
        url_list.append("https://www.onlinelibrary.wiley.com/toc/16163028/" + str(1961 + int(iss[0])) + "/" + str(int(iss[0])) + "/" + str(int(iss[1])))
        print(url_list)
    paper_url_list = []
    for url in url_list:
        paper_url = get_latest_issue_inf(url)
        for paper_url_1 in paper_url:
            paper_url_list.append(paper_url_1)
    print(len(paper_url_list))
    paper_url_list = compare_url(paper_url_list, "data\\Wiley_Angew.csv", "data\\Temp\\Wiley_Angew.csv")
    print(len(paper_url_list))
    if len(paper_url_list) > 0:
        paper_title_list = ["a" for _x in range(len(paper_url_list))]
        paper_abstract_list = ["a" for _x in range(len(paper_url_list))]
        for i in range(0, len(paper_url_list)):
            print(paper_url_list[i])
            [paper_title_list[i], paper_abstract_list[i]] = get_abstract(paper_url_list[i])
            # print(paper_abstract_list[i])
        return paper_title_list, paper_url_list, paper_abstract_list, latest_issue
    else:
        paper_title_list = []
        paper_url_list = []
        paper_abstract_list = []
        return paper_title_list, paper_url_list, paper_abstract_list, latest_issue

#ISS = 'Vol. 59, Iss. 26'
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_Wiley_Angew(ISS)
#print(paper_title_list)
#print(paper_url_list)
#print(paper_abstract_list)

