import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os
import platform
from soynlp.noun import LRNounExtractor

# --- 한글 폰트 설정 (운영체제별) ---
if platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
elif platform.system() == 'Windows':  # Windows
    plt.rc('font', family='Malgun Gothic')
else:
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False

# --- 파일 불러오기 ---
file_path = "./data/news-contents.csv"
df = pd.read_csv(file_path)

# --- 불용어 정의 ---
stopwords = set([
    '것', '수', '등', '더', '를', '의', '에', '가', '이', '은', '는', '다', '도', '으로', '하고', '에서', '기사', '기자', '뉴스'
    # 필요시 확장
])

# --- 명사 추출 함수 ---
def extract_nouns_soynlp(texts):
    noun_extractor = LRNounExtractor()
    noun_extractor.train(texts)
    nouns_scores = noun_extractor.extract()
    nouns = list(nouns_scores.keys())
    return [n for n in nouns if n not in stopwords and len(n) > 1]

# --- 전체 뉴스 내용 결합 ---
all_texts = df['content'].dropna().astype(str).tolist()

# --- 명사 추출 및 카운팅 ---
nouns = extract_nouns_soynlp(all_texts)
counts = Counter()

for text in all_texts:
    for noun in nouns:
        counts[noun] += text.count(noun)

# --- 중복 (3회 이상) 명사 중 상위 20개 추출 ---
repeated = {word: cnt for word, cnt in counts.items() if cnt >= 3}
top20 = dict(Counter(repeated).most_common(20))

# --- 시각화 저장 폴더 ---
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# --- 워드클라우드 ---
wc = WordCloud(
    font_path="NanumGothic.ttf",  # 시스템에 맞게 수정
    background_color='white',
    width=800,
    height=400
).generate_from_frequencies(top20)

plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title("전체 뉴스 중복 명사 상위 20개 워드클라우드")
plt.tight_layout()
plt.savefig(f"{output_dir}/전체_중복명사_top20_wordcloud.png")
plt.close()

# --- 막대그래프 ---
words, counts_vals = zip(*top20.items())
plt.figure(figsize=(10, 5))
plt.bar(words, counts_vals, color='skyblue')
plt.title("전체 뉴스 중복 명사 상위 20개")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{output_dir}/전체_중복명사_top20_bargraph.png")
plt.close()

print("전체 뉴스 기준 중복 명사 상위 20개 시각화 완료.")
