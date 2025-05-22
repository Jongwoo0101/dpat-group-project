import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re
import os

# matplotlib 한글 깨짐 방지
import platform

# 운영체제별 폰트 설정
if platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    plt.rc('font', family='Malgun Gothic')
else:  # Linux (colab 등)
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False

# 뉴스 데이터 불러오기 (파일 경로에 맞게 수정)
file_path = "src/news/news_data.csv"
df = pd.read_csv(file_path)

# 한글 키워드 추출 함수
def extract_keywords(texts):
    all_text = ' '.join(texts.dropna().astype(str))
    words = re.findall(r'[가-힣]{2,}', all_text)
    return Counter(words)

# 날짜 컬럼 기준으로 키워드 추출 및 시각화
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

for date in df.columns:
    keywords = extract_keywords(df[date])
    
    if not keywords:
        print(f"{date}: 키워드 없음")
        continue

    # 상위 키워드 20개
    top_keywords = keywords.most_common(20)

    # 워드클라우드 생성
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
    plt.savefig(f"{output_dir}/{date}_wordcloud.png")
    plt.close()

    # 시각화: 막대그래프
    words, counts = zip(*top_keywords)
    plt.figure(figsize=(10, 5))
    plt.bar(words, counts, color='skyblue')
    plt.title(f"{date} 주요 키워드")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{date}_bargraph.png")
    plt.close()

    print(f"{date}: 시각화 완료")

print(f"모든 날짜의 시각화 결과가 '{output_dir}' 폴더에 저장되었습니다.")
