import requests
from bs4 import BeautifulSoup
import re
import random,time
from compare_url_title_abstract import compare_url_title_abstract

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
    each_paper_url = soup.findAll("a", {'data-track-action': "view volume"})
    #each_paper_url = soup.findAll("div", {'class': "highwire-cite-highlight"})
    #print(each_paper_url)
    #print(each_paper_url[len(each_paper_url)-1])
    pattern1 = r'.*href="(.*)">.*'
    pattern2 = r'\d+'
    url = str(re.findall(pattern1, str(each_paper_url[0]))).replace("['", "").replace("']", "")
    volume_url = ("https://www.nature.com" + str(url))
    content = get_content(volume_url)
    soup = BeautifulSoup(content, 'html.parser')
    each_paper_url = soup.findAll("a", {'data-track-action': "view issue"})
    url = str(re.findall(pattern1, str(each_paper_url[0]))).replace("['", "").replace("']", "")
    k = re.findall(pattern2, str(url))
    latest_issue_inf = ("Vol. " + str(k[0].replace("['", "").replace("']", "")) + ", Iss. "+str(k[1].replace("['", "").replace("']", "")))
    latest_issue_url = ("https://www.nature.com"+str(url))
    #print(latest_issue_url)
    #print(latest_issue_inf)
    return latest_issue_inf, latest_issue_url


def get_latest_issue_inf(url):
    content = get_content(url)
    soup = BeautifulSoup(content, 'html.parser')
    #print(soup)
    #each_paper_url = soup.findAll("h3", {'class': "mb10 extra-tight-line-height"})
    #each_paper_abs = soup.findAll("div", {'itemprop': "description"})
    each_paper_url = soup.findAll("article")
    #print(each_paper_url)
    #print(len(each_paper_url))
    pattern1 = r'.*href="(.*)" itemprop.*'
    pattern2 = r'.*      (.*)</a>.*'
    pattern3 = r'.*<p>(.*)</p>.*'
    pattern4 = r'.*<.*>.*'
    paper_url_list = []
    paper_title_list = []
    paper_abstract_list = []
    for paper in each_paper_url:
        #print(paper)
        paper_url_list.append("https://www.nature.com" + str(str(re.findall(pattern1, str(paper))).replace("[", "").replace("]", "").replace("'", "")))
        paper_title_list.append(str(re.findall(pattern2, str(paper))).replace("['", "").replace("']", "").replace("'", ""))
        paper_abstract_list.append(str(re.sub(pattern4, "", str(re.findall(pattern3, str(paper))), count=0)).replace("['", "").replace("']", "").replace("'", ""))
    #print(paper_url_list)
    #print(len(paper_url_list))
    #print(paper_title_list)
    #print(len(paper_title_list))
    #print(paper_abstract_list)
    #print(len(paper_abstract_list))
    return paper_url_list, paper_title_list, paper_abstract_list


def spider_Nature_nanotechnology(ISS):
    url = ("https://www.nature.com/nnano/volumes")
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
        url_list.append("https://www.nature.com/nnano/volumes/" + str(int(iss[0])) + "/issues/" + str(int(iss[1])))
        print(url_list)
    paper_url_list = []
    paper_title_list = []
    paper_abstract_list = []
    for url in url_list:
        [paper_url, paper_title, paper_abstract] = get_latest_issue_inf(url)
        for paper_url_1 in paper_url:
            paper_url_list.append(paper_url_1)
        for paper_title_1 in paper_title:
            paper_title_list.append(paper_title_1)
        for paper_abstract_1 in paper_abstract:
            paper_abstract_list.append(paper_abstract_1)
    print(len(paper_url_list))
    [paper_url_list, paper_title_list, paper_abstract_list] = compare_url_title_abstract(paper_url_list, paper_title_list, paper_abstract_list, "data\\Nature_nanotechnology.csv", "data\\Temp\\Nature_nanotechnology.csv")
    print(len(paper_url_list))
    return paper_title_list, paper_url_list, paper_abstract_list, latest_issue


#ISS = 'Vol. 16, Iss. 9'
#[paper_title_list, paper_url_list, paper_abstract_list, latest_issue] = spider_Nature_nanotechnology(ISS)
#print(paper_title_list)
#print(paper_url_list)
#print(paper_abstract_list)
#print(len(paper_abstract_list))
