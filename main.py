# This is a sample Python script.
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


tlist=[]
link =[]
gulist=[]
for page in range(100):
    raw = requests.get('https://search.naver.com/search.naver?date_from=&date_option=0&date_to=&dup_remove=1&nso=&post_blogurl=&post_blogurl_without=&query=%EC%9C%A1%EC%95%84%20%EB%82%B4%EC%9A%A9&sm=tab_pge&srchby=all&st=sim&where=post&start='+str(page * 10 + 1)).text
    soup = BeautifulSoup(raw, 'html.parser')
    my_titles = soup.select(
        'dl > dt > a'
    )


    ## my_titles는 list 객체
    for title in my_titles:

        if "지원" in title.text:
            gubnText = '#지원'
        else :
            gubnText = ''
        tlist.append(title.text)
        link.append(title.get('href'))
        gulist.append(gubnText)




    #새로운값
    index_format = tlist
    columns_format = ['구분', '링크']
    values = pd.DataFrame(index=index_format, columns=columns_format)
    print(values)

    # x & y 값 정의
    x = gulist
    y = link


    for ii in range(values.shape[0]):
        # fill in x values into column index zero of values
        values.iloc[ii, 0] = x[ii]
        # fill in x values into column index one of values
        values.iloc[ii, 1] = y[ii]



    values.to_excel('./test.xlsx',
                    sheet_name='Sheet1',
                    columns=columns_format,
                    header=True,
                    index=index_format,
                    index_label="제목",
                    startrow=1,
                    startcol=0,
                    engine=None,
                    merge_cells=True,
                    encoding=None,
                    inf_rep='inf',
                    verbose=True,
                    freeze_panes=None)







