import pandas
import numpy as np

def compare_url_title(url, title, csv, csv1):
    url_old = pandas.read_csv(csv, skiprows=0)
    new_url_list = []
    new_title_list = []
    for j in range(0, len(url)):
        ISNEW = 0
        for i in range(0, len(url_old)):
            if str(url_old['url'][i]) == str(url[j]):
                ISNEW = 1
        if ISNEW == 0:
            new_url_list.append(url[j])
            new_title_list.append(title[j])
    df = pandas.DataFrame(np.random.rand(len(url)).reshape(len(url), 1), columns={"url"})
    for i in range(0, len(url)):
        df['url'][i] = url[i]
    df.to_csv(csv1, header=True, index=False)

    return new_url_list, new_title_list

