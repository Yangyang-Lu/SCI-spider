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
    #print(content)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("div", {'class': "parent-item"})
    #print(each_paper_url[0])
    pattern1 = r'.*<a href="(.*)"><span class.*'
    pattern2 = r'\d+'
    url = str(re.findall(pattern1, str(each_paper_url[0]))).replace("['", "").replace("']", "")
    k = re.findall(pattern2, str(url))
    latest_issue_inf = ("Vol. "+str(k[0])+", Iss. "+str(k[1]))
    latest_issue_url = ("https://pubs.acs.org"+str(url))
    #print(latest_issue_url)
    #print(latest_issue_inf)
    return latest_issue_inf, latest_issue_url


def get_latest_issue_inf(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    #print(soup)
    each_paper_url = soup.findAll("h5", {'class': "issue-item_title"})
    #each_paper_url = soup.findAll("div")
    #print(each_paper_url)
    #print(len(each_paper_url))
    pattern1 = r'.*a href="(.*?)" title.*'
    pattern2 = r'.*">(.*)</a></h5>.*'
    pattern3 = r'<.*?>'
    paper_url_list = []
    paper_title_list = []
    for paper in each_paper_url:
       # print(paper)
        #paper_url_list.append("https://pubs.acs.org/"+str(paper_url.replace('full', 'abs')))
        k = str(re.findall('">.*', str(str(re.findall(pattern1, str(paper)))))).replace("'", "").replace("[", "").replace("]",  "").replace("\\", "")

        paper_url_list.append("https://pubs.acs.org" + str(str(re.findall(pattern1, str(paper))).replace(k, "").replace("[", "").replace("]", "").replace("'", "")))
        paper_title_list.append((re.sub(pattern3, "", str(re.findall(pattern2, str(paper))), count=0)).replace("['", "").replace("']", "").replace("'", ""))
    #print(paper_url_list)
    #print(len(paper_url_list))
    #print(paper_title_list)
    #print(len(paper_title_list))
    return paper_url_list, paper_title_list


def get_abstract(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')

    each_paper_url = soup.findAll("p", {'class': "articleBody_abstractText"})
    #print(each_paper_url)
    pattern1 = r'.*<p class="articleBody_abstractText">(.*)</p>.*'
    pattern2 = r'<.*?>'
    latest_issue_inf = re.sub(pattern2, '', str(re.findall(pattern1, str(each_paper_url))), count=0).replace("['", "")
    #print(latest_issue_inf)
    return str(latest_issue_inf)


def spider_ACS_NANOLetters(ISS):
    url = ("https://pubs.acs.org/loi/nalefd")
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
        url_list.append("https://pubs.acs.org/toc/nalefd/" + str(int(iss[0])) + "/" +str(int(iss[1])))
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
    [paper_url_list, paper_title_list] = compare_url_title(paper_url_list, paper_title_list, "data\\ACS_NANOLetters.csv", "data\\Temp\\ACS_NANOLetters.csv")
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




#ISS = 'Vol. 20, Iss. 5'
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_ACS_NANOLetters(ISS)
#print(latest_issue)
#print(paper_title_list)
#print(paper_url_list)
#print(paper_abstract_list)
#print(len(paper_abstract_list))