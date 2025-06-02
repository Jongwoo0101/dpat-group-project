import pandas as pd

df = pd.read_csv("./data/coin_data.csv")  # 파일명을 실제 경로에 맞게 사용하세요

# '캔들 기준 시각(UTC기준)'을 datetime으로 변환
df['캔들 기준 시각(UTC기준)'] = pd.to_datetime(df['캔들 기준 시각(UTC기준)'])
df['전일 종가 대비 변화량의 절댓값'] = df['전일 종가 대비 변화량의 절댓값'] * 100
# 2024년 9월 1일부터 12월 31일까지 필터링
start_date = '2024-01-01'
end_date = '2024-12-31'

filtered_df = df[(df['캔들 기준 시각(UTC기준)'] >= start_date) & (df['캔들 기준 시각(UTC기준)'] <= end_date)]

# 날짜 기준 오름차순 정렬
filtered_df = filtered_df.sort_values(by='캔들 기준 시각(UTC기준)', ascending=True)

# CSV로 저장
filtered_df.to_csv("filtered_BTC_data_2024_Sep_Dec.csv", index=False)
