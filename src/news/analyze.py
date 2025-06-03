import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import platform
from datetime import datetime
from soynlp.noun import LRNounExtractor

# --- 한글 폰트 설정 (운영체제별) ---
if platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    plt.rc('font', family='Malgun Gothic')
else:
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False

# --- 데이터 불러오기 (파일 경로에 맞게 수정) ---
file_path = "./data/news-contents.csv"
df = pd.read_csv(file_path)

# --- 불용어 리스트 정의 ---
stopwords = set([
    '것', '수', '등', '더', '를', '의', '에', '가', '이', '은', '는', '다', '도', '으로', '하고', '에서',
    # 필요시 추가
])

# --- 날짜 포맷 변환 함수 (YYYY-MM-DD HH:MM:SS -> MM월 DD일) ---
def format_date(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%m월 %d일")

# --- 명사 추출 함수 (soynlp) ---
def extract_nouns_soynlp(texts):
    noun_extractor = LRNounExtractor()
    noun_extractor.train(texts)
    nouns_scores = noun_extractor.extract()

    # 명사 리스트만 추출
    nouns = list(nouns_scores.keys())

    # 불용어 제거 및 2자 이상 필터링
    meaningful_nouns = [noun for noun in nouns if noun not in stopwords and len(noun) > 1]
    return meaningful_nouns

# --- 결과 저장 폴더 ---
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# --- 날짜별 키워드 분석 ---
for date, group in df.groupby('date'):
    contents = group['content'].dropna().astype(str).tolist()

    # soynlp는 리스트 형태 훈련 데이터로 받음
    nouns = extract_nouns_soynlp(contents)
    counts = Counter()

    # 각 기사별 명사 개수 세기 (soynlp는 명사 후보 추출, 여기선 전체 텍스트에서 추출된 명사들의 출현 빈도를 세기 위해 따로 처리)
    for text in contents:
        for noun in nouns:
            counts[noun] += text.count(noun)

    # 3회 이상 반복 명사 필터링
    repeated = {word: cnt for word, cnt in counts.items() if cnt >= 3}

    if not repeated:
        print(f"{date}: 반복 명사 없음")
        continue

    top20 = dict(Counter(repeated).most_common(20))
    date_fmt = format_date(date)

    # 워드클라우드 생성
    wc = WordCloud(
        font_path="NanumGothic.ttf",  # 시스템에 맞게 경로 조정
        background_color='white',
        width=800,
        height=400
    ).generate_from_frequencies(top20)

    plt.figure(figsize=(10,5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"{date_fmt} 상위 20개 명사 워드클라우드")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{date_fmt}top20키워드_워드클라우드.png")
    plt.close()

    # 막대그래프 생성
    words, counts_vals = zip(*top20.items())
    plt.figure(figsize=(10,5))
    plt.bar(words, counts_vals, color='skyblue')
    plt.title(f"{date_fmt} 상위 20개 명사 빈도")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/{date_fmt}top20키워드_막대그래프.png")
    plt.close()

    print(f"{date_fmt}: 상위 20개 명사 시각화 완료")

print(f"모든 날짜별 상위 20개 명사 시각화가 '{output_dir}'에 저장되었습니다.")
