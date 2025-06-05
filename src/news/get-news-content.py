import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import re
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'}
# with open ("./links_with_title.txt", "r", encoding= "utf-8") as file:
#     tempList= file.readline().split("AAAAA")
#     news_date=tempList[0]
#     news_url= tempList[1]
#     news_title= tempList[2]
# print(news_date)
# print(news_url)
# print(news_title)
# driver= webdriver.Chrome()
# driver.get(news_url)
# time.sleep(10)
# soup= BeautifulSoup(driver.page_source, 'html.parser')
# content= soup.select_one(".article-body-text").text
# print(content)
# driver.close()
date_lists=[]
url_lists=[]
title_lists=[]
content_lists=[]

def get_news_content():
    with open('./data/links_with_title.txt', 'r') as file:
        for i in file.readlines():
            tempList= i.split("AAAAA")
            date_lists.append(tempList[0])
            url_lists.append(tempList[1])
            title_lists.append(tempList[2])
    for url in url_lists:
        driver= webdriver.Safari()
        driver.get(url)
        time.sleep(3)
        soup= BeautifulSoup(driver.page_source, 'html.parser')
        content= soup.select_one(".article-body-text").text
        content_split= re.split(r'ADVERTISEMENT|연합뉴스 TV',content)
        content_real= content_split[0]+content_split[1]
        print(content_real)
        content_lists.append(content_real)
        driver.close()

def make_csv():
    comment_list_zip=list(
        zip(date_lists, title_lists, content_lists, url_lists)
    )
    cols= ['date', 'title', 'content', 'url']
    df= pd.DataFrame(comment_list_zip, columns=cols)
    df.to_csv('./data/news_contents.csv', index=False)


get_news_content()
make_csv()

