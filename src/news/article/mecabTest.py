import datetime

import MeCab
import pandas as pd
import re
import os
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import platform

# 운영체제별 폰트 설정
if platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    plt.rc('font', family='Malgun Gothic')
else:  # Linux (colab 등)
    plt.rc('font', family='NanumGothic')
tagger = MeCab.Tagger(
    "-r /opt/homebrew/etc/mecabrc -d /opt/homebrew/lib/mecab/dic/mecab-ko-dic"
)
file_path ="./news-contents.csv"
df = pd.read_csv(file_path)

def extract_keywords(all_content, tagger):
    nouns = []
    for text in all_content:
        # print(text)
        node = tagger.parseToNode(text)
        while node:
            surface = node.surface.strip()
            if (("NNG" in node.feature or "NNP" in node.feature) and len(surface) >= 2):
                nouns.append(surface)
            node = node.next
    return Counter(nouns)

def analyze_content():
    dateDf = pd.read_csv("../../data/filtered_BTC_data_2024_date.csv")
    date_list = []
    for i in dateDf['캔들 기준 시각(UTC기준)'].values.tolist():
        date_list.append(
            datetime.datetime.strptime(i, '%Y-%m-%d')
        )
    date_list.reverse()

    for date_datetime in date_list:
        date=date_datetime.strftime('%Y-%m-%d %H:%M:%S')
        print(date)
        df2=df[df['date']==date]
        all_content = []
        for content_text in df2['content']:

            content_text2 = re.sub(r'(기자|기사|문의|카톡|라인|연합뉴스|제보|연합뉴스TV|jebo23\(끝\)|앵커|리뷰|리포터)', '', content_text).strip()
            # print(content_text2)
            all_content.append(content_text2)

        output_dir = "output2"
        os.makedirs(output_dir, exist_ok=True)
        keywords = extract_keywords(all_content, tagger)
        top_keywords = keywords.most_common(30)

        wc = WordCloud(
            font_path="src/news/NanumGothic.ttf",  # 시스템에 맞게 경로 조정
            background_color='white',
            width=800,
            height=400
        ).generate_from_frequencies(dict(top_keywords))

        # 시각화: 워드클라우드
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"{date} 워드클라우드")
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{date}_1_wordcloud.png")
        plt.close()

        # 시각화: 막대그래프
        words, counts = zip(*top_keywords)
        plt.figure(figsize=(10, 5))
        plt.bar(words, counts, color='skyblue')
        plt.title(f"{date} 주요 키워드")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{date}_1_bargraph.png")
        plt.close()

        print(f"{date}: 시각화 완료")

analyze_content()

# df2 = df[df['date'] == '2024-01-08 00:00:00']
# for content_text in df2['content']:
#
#     content_text2=re.sub(r'(기자|기사|문의|카톡|라인|연합뉴스|제보|연합뉴스TV|jebo23\(끝\)|앵커|리뷰|리포터)', '', content_text).strip()
#     print(content_text2)
#     all_content.append(content_text2)

# output_dir = "output2"
# os.makedirs(output_dir, exist_ok=True)
# keywords= extract_keywords(all_content,tagger)
# top_keywords = keywords.most_common(30)
# date='2024-01-08 00:00:00'
# wc = WordCloud(
#     font_path="src/news/NanumGothic.ttf",  # 시스템에 맞게 경로 조정
#     background_color='white',
#     width=800,
#     height=400
# ).generate_from_frequencies(dict(top_keywords))
#
# # 시각화: 워드클라우드
# plt.figure(figsize=(10, 5))
# plt.imshow(wc, interpolation='bilinear')
# plt.axis('off')
# plt.title(f"{date} 워드클라우드")
# plt.tight_layout()
# plt.savefig(f"{output_dir}/{date}_1_wordcloud.png")
# plt.close()
#
# # 시각화: 막대그래프
# words, counts = zip(*top_keywords)
# plt.figure(figsize=(10, 5))
# plt.bar(words, counts, color='skyblue')
# plt.title(f"{date} 주요 키워드")
# plt.xticks(rotation=45, ha='right')
# plt.tight_layout()
# plt.savefig(f"{output_dir}/{date}_1_bargraph.png")
# plt.close()
#
# print(f"{date}: 시각화 완료")
