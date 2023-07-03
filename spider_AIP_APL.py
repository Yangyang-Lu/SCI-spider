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
    each_paper_url = soup.findAll("li", {'class': "row js_issue"})
    k = ("Vol. "+str(each_paper_url[0].get('data-volume'))+", Iss. "+str(each_paper_url[0].get('data-issue')))
    url = ("https://aip.scitation.org/toc/apl/"+str(each_paper_url[0].get('data-volume'))+"/"+str(each_paper_url[0].get('data-issue')))
    #print(k)
    #print(url)
    return str(k), str(url)


def get_latest_issue_inf(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    #print(soup)
    each_paper_url = soup.findAll("a", {'class': "ref nowrap"})
    #print(each_paper_url)

    pattern2 = r'.*hlFld-Title">(.*)</h4></a>.*'
    paper_url_list = []
    paper_title_list = []
    for paper in each_paper_url:
        paper_url = paper.get('href')
        #paper_url_list.append("https://aip.scitation.org"+str(paper_url.replace('full', 'abs')))
        paper_url_list.append("https://aip.scitation.org" + str(paper_url))
        paper_title_list.append(str(re.findall(pattern2, str(paper))).replace("['", "").replace("']", "").replace("</sub>", "").replace("<sub>", ""))
    #print(paper_url_list)
    #print(len(paper_url_list))
    #print(paper_title_list)
    #print(len(paper_title_list))
    return paper_url_list, paper_title_list


def get_abstract(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("div", {'class': "NLM_paragraph"})
    #print(each_paper_url[0])
    pattern1 = r'.*<div class="NLM_paragraph">(.*)</div>.*'
    pattern2 = r'<.*?>'
    if len(each_paper_url) > 0:
        latest_issue_inf = re.sub(pattern2, "", str(re.findall(pattern1, str(each_paper_url[0]))), count=0).replace("['", "").replace("']", "")
    else:
        latest_issue_inf = "None"
    #print(latest_issue_inf)
    return latest_issue_inf


def spider_AIP_APL(ISS):
    url = ("https://aip.scitation.org/toc/apl/current")
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
        url_list.append("https://aip.scitation.org/toc/apl/" + str(int(iss[0])) + "/" + str(int(iss[1])))
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
    [paper_url_list, paper_title_list] = compare_url_title(paper_url_list, paper_title_list, "data\\AIP_APL.csv", "data\\Temp\\AIP_APL.csv")
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



#ISS = 'Vol. 116, Iss. 23'
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_AIP_APL(ISS)
#print(paper_title_list)
#print(paper_url_list)
#print(paper_abstract_list)

