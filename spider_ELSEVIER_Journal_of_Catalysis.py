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
    each_paper_url = soup.findAll("a", {'class': "anchor js-issue-item-link text-m"})
    #print(each_paper_url)
    pattern2 = r'.*/journal-of-catalysis/vol/(.*)/suppl/C.*'
    vol = ('Vol. ' + str(re.findall(pattern2, str(each_paper_url[0]))).replace("['", '').replace("']", "") + "-" + str(int(str(
        re.findall(pattern2, str(each_paper_url[0]))).replace("['", '').replace("']", "")) - 1))
    vol1 = str(re.findall(pattern2, str(each_paper_url[0]))).replace("['", '').replace("']", "")
    vol2 = str(int(str(re.findall(pattern2, str(each_paper_url[0]))).replace("['", '').replace("']", "")) - 1)
    url = []
    url.append("https://www.sciencedirect.com/journal/journal-of-catalysis/vol/" + str(vol1) + "/suppl/C")
    url.append("https://www.sciencedirect.com/journal/journal-of-catalysis/vol/" + str(vol2) + "/suppl/C")
    #print(url)
    return str(vol), url


def get_latest_issue_inf(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("h3", {'class': "text-m u-font-serif u-display-inline"})
    #print(each_paper_url)
    pattern1 = r'.*href="(.*)" id=".*'
    pattern2 = r'.*<span class="js-article-title">(.*)</span></span>.*'
    paper_url_list = []
    paper_title_list = []
    for paper in each_paper_url:
        paper_url_list.append("https://www.sciencedirect.com/" + str(str(re.findall(pattern1, str(paper))).replace("['", '').replace("']", "")))
        paper_title_list.append(str(re.findall(pattern2, str(paper))).replace("</sub>", '').replace("<sub>", '').replace("['", '').replace("']", ''))
    #print(paper_url_list)
    #print(len(paper_url_list))
    #print(paper_title_list)
    #print(len(paper_title_list))
    return paper_url_list, paper_title_list


def get_abstract(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')

    each_paper_url = soup.findAll("div", {'class': "abstract author"})
    #print(each_paper_url)
    pattern1 = r'<.*?>'
    if len(each_paper_url)>0:
        paper_abstract_list = str(re.sub(pattern1, '', str(each_paper_url[0]), count=0)).replace("Abstract", "")
    else:
        paper_abstract_list = ''
    #print(paper_abstract_list)
    return str(paper_abstract_list)


def spider_ELSEVIER_Journal_of_Catalysis(ISS):
    url = ("https://www.sciencedirect.com/journal/journal-of-catalysis/issues")
    [latest_issue, latest_issue_url] = get_page(url)
    print(latest_issue_url)
    print(latest_issue)
    if latest_issue == ISS:
        url_list = []
        url_list.append(str(latest_issue_url[0]))
        url_list.append(str(latest_issue_url[1]))
        print(url_list)
    else:
        url_list = []
        url_list.append(str(latest_issue_url[0]))
        url_list.append(str(latest_issue_url[1]))
        pattern1 = r'\d+'
        iss = re.findall(pattern1, str(ISS))
        url_list.append("https://www.sciencedirect.com/journal/journal-of-catalysis/vol/" + str(int(iss[0])) + "/suppl/C")
        url_list.append("https://www.sciencedirect.com/journal/journal-of-catalysis/vol/" + str(int(iss[1])) + "/suppl/C")
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
    [paper_url_list, paper_title_list] = compare_url_title(paper_url_list, paper_title_list, "data\\ELSEVIER_Journal_of_Catalysis.csv", "data\\Temp\\ELSEVIER_Journal_of_Catalysis.csv")
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





#ISS = 'Vol. 392-391'
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_ELSEVIER_Journal_of_Catalysis(ISS)
#print(paper_title_list)
#print(paper_url_list)
#print(paper_abstract_list)
#print(len(paper_abstract_list))