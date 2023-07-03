import pandas
import numpy as np

def compare_url(url, csv, csv1):
    url_old = pandas.read_csv(csv, skiprows=0)
    new_url_list = []
    for url_1 in url:
        ISNEW = 0
        for i in range(0, len(url_old)):
            if str(url_old['url'][i]) == str(url_1):
                ISNEW = 1
        if ISNEW == 0:
            new_url_list.append(url_1)
    df = pandas.DataFrame(np.random.rand(len(url)).reshape(len(url), 1), columns={"url"})
    for i in range(0, len(url)):
        df['url'][i] = url[i]
    df.to_csv(csv1, header=True, index=False)

    return new_url_list

