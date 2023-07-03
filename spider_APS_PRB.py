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


def get_vol_iss(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("div", {'class': "current-issue"})
    #print(each_paper_url)
    pattern2 = r'.*<p>(.*)</p>.*'
    latest_issue = re.findall(pattern2, str(each_paper_url[0]))
    #print(latest_issue)
    pattern1 = r'\d+'
    vol_iss = re.findall(pattern1, str(latest_issue))
    latest_issue_url = []
    for i in range(int(vol_iss[1]), (int(vol_iss[2])+1)):
        latest_issue_url.append("/prb/issues/" + str(vol_iss[0]) + "/" + str(int(i)))
    latest_issue_inf = ("Vol. " + str(vol_iss[0]) + ", Iss. " + str(vol_iss[1]) + "-" + str(vol_iss[2]))
    return str(latest_issue_inf), latest_issue_url


def get_abstract(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_abstract = soup.findAll("p")
    each_paper_title = soup.findAll("title")
    #print(each_paper_abstract[0])
    #print(each_paper_title[0])
    pattern1 = r'.*<p>(.*)</p>.*'
    pattern2 = r'.* - (.*)</title>.*'
    pattern3 = r'<.*?>'
    if len(each_paper_abstract)> 0:
        paper_abstract = re.sub(pattern3, "", str(re.findall(pattern1, str(each_paper_abstract[0]))), count=0).replace(
            "['", "").replace("']", "").replace('\u2009', '').replace('["', "").replace('"]', "")
    else:
        paper_abstract = " "
    #paper_abstract = re.sub(pattern3, "", str(re.findall(pattern1, str(each_paper_abstract[0]))), count=0).replace("['", "").replace("']", "").replace('\u2009', '').replace('["', "").replace('"]', "")
    paper_title = str(re.findall(pattern2, str(each_paper_title[0]))).replace("['", "").replace("']", "").replace("$", "").replace("{", "").replace("}", "").replace("\\", "").replace("mathrm", "").replace("_", "")
    #print(paper_abstract)
    #print(paper_abstract)
    #print(paper_title)
    return str(paper_title), str(paper_abstract)


def get_latest_issue_inf(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("a", {'class': "tiny button right-button"})
    #print(each_paper_url)
    paper_url_list = []
    for paper in each_paper_url:
        paper = paper.get('href')
        paper_url_list.append(paper)
        #print(paper)
    return paper_url_list


def spider_APS_PRB(ISS):
    url = ("https://journals.aps.org/prb/")
    [latest_issue, latest_issue_url] = get_vol_iss(url)
    print(latest_issue_url)
    print(latest_issue)

    if latest_issue == ISS:
        url_list = []
        for latest_issue_url_1 in latest_issue_url:
            url_list.append("https://journals.aps.org" + str(latest_issue_url_1))
        print(url_list)
    else:
        url_list = []
        for latest_issue_url_1 in latest_issue_url:
            url_list.append("https://journals.aps.org" + str(latest_issue_url_1))
        pattern1 = r'\d+'
        iss = re.findall(pattern1, str(ISS))
        for i in range(int(iss[1]), (int(iss[2]) + 1)):
            url_list.append("https://journals.aps.org/prb/issues/" + str(int(iss[0])) + "/" + str(int(i)))
        print(url_list)
    paper_url_list = []
    for url in url_list:
        paper_url = get_latest_issue_inf(url)
        for paper_url_1 in paper_url:
            paper_url_list.append(paper_url_1)

    print(len(paper_url_list))
    paper_url_list = compare_url(paper_url_list, "data\\APS_PRB.csv", "data\\Temp\\APS_PRB.csv")
    print(len(paper_url_list))

    if len(paper_url_list) > 0:
        # print(paper_url_list)
        for i in range(0, len(paper_url_list)):
            paper_url_list[i] = ("https://journals.aps.org" + str(paper_url_list[i]))
            # print(paper_url_list[i])
        print(len(paper_url_list))
        paper_title_list = ["a" for _x in range(len(paper_url_list))]
        paper_abstract_list = ["a" for _x in range(len(paper_url_list))]
        for i in range(0, len(paper_url_list)):
            print(paper_url_list[i])
            [paper_title_list[i], paper_abstract_list[i]] = get_abstract(paper_url_list[i])
            # print(paper_title_list[i])
            # print(paper_abstract_list[i])
        return paper_title_list, paper_url_list, paper_abstract_list, latest_issue
    else:
        paper_title_list = []
        paper_url_list = []
        paper_abstract_list = []
        return paper_title_list, paper_url_list, paper_abstract_list, latest_issue


#ISS = 'Vol. 105, Iss. 5-8'
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_APS_PRB(ISS)