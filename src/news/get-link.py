import requests
import feedparser
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import datetime
from selenium.webdriver.common.keys import Keys

def get_date():
    df=pd.read_csv("../coin/data/filtered_BTC_data_2024.csv")

    # df1=df['캔들 기준 시각(UTC기준)']
    # date_list= df1.values.tolist()
    date_list=[]
    for i in df['캔들 기준 시각(UTC기준)'].values.tolist():
        date_list.append(
            datetime.datetime.strptime(i,'%Y-%m-%d')
        )
    date_list.reverse()
    diffMonth_day=[]
    now= datetime.datetime.now()

    for i in date_list:
        diffMonth=(now.year - i.year) *12 +(now.month-i.month)
        diffMonth_day.append([diffMonth,i.day])
        now= i
    print(diffMonth_day)

    return diffMonth_day, date_list






get_date()

def ypnews(diffMonth_day,date_list):
    date_list_count=0
    driver=webdriver.Chrome()
    driver.get("https://www.yonhapnewstv.co.kr/news?ct=6")
    time.sleep(7)
    driver.find_element(By.CSS_SELECTOR,"input[title='조회순 정렬']").click()

    for i in diffMonth_day:
        driver.find_element(By.CSS_SELECTOR,".ui-datepicker-trigger").click()
        for loop in range(i[0]):# < 눌러서 원하는 날짜의 달까지 가기
            time.sleep(0.3)
            driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-prev").click()

        # element= driver.find_element(By.CSS_SELECTOR, "table.ui-datepicker-calendar")

        elements= driver.find_elements(By.CSS_SELECTOR, 'td[data-event="click"]>a[href="#"]')
        for element in elements:
            if(element.text ==str(i[1])):
                element.click()
                break

        #여기까지 날짜 선택 누름
        time.sleep(1)
        soup2=BeautifulSoup(driver.page_source,'html.parser')
        # atags=soup2.find_all('ul.article-webzine>li>div.item-body')

        links= soup2.select('ul.article-webzine>li>div>div.item-body>a.title')
        hrefs = [tag['href'] for tag in links]
        title= [tag.get_text(strip=True) for tag in links]

        for j in range(len(hrefs)):
            with open("./links_with_title.txt", "a") as file:
                file.write(
                    str(date_list[date_list_count])
                    +"AAAAA"
                    +"https://www.yonhapnewstv.co.kr"+hrefs[j]
                    +"AAAAA"+title[j]+"\n"
                            )
        date_list_count+=1




datediff,date_list= get_date()
ypnews(datediff, date_list)








