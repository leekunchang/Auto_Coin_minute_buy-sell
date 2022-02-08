import pyupbit
import numpy as np

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-XRP","minute60",72)

# 이동평균선 5분 기준 추가(window=고려일수)
df['ma5'] = df['close'].rolling(window=5).mean()

# 이평선 5분 전봉
df['ma5_1'] = df['close'].rolling(window=5).mean().shift(1)

# 이평선 5분 2전봉
df['ma5_2'] = df['close'].rolling(window=5).mean().shift(2)

# 이동평균선 10분 기준 추가(window=고려일수)
df['ma10'] = df['close'].rolling(window=10).mean()

# 이평선 10분 전봉
df['ma10_1'] = df['close'].rolling(window=10).mean().shift(1)

# 이평선 10분 2전봉
df['ma10_2'] = df['close'].rolling(window=10).mean().shift(2)

# # ma5 > ma10 and ma5 > ma5_1
# df['ma5 > ma10 and ma5 > ma5_1'] = np.where(df['ma5'] > df['ma10'] & df['ma5'] > df['ma5_1'], 1, 0)

# # ma5 > ma10 and ma5 > ma5_1 > ma5_2 3시간전부터 지속적인 상승추세
# df['ma5>ma10 and ma5 > ma5_1 > ma5_2'] = np.where(df['ma5'] > df['ma10'] & df['ma5'] > df['ma5_1'] > df['ma5_2'], 1, 0)

# # 이동평균선 5분 기준 추가(window=고려일수)
# df['ma20'] = df['close'].rolling(window=20).mean()

# # 이동평균선 5분 기준 추가(window=고려일수)
# df['ma60'] = df['close'].rolling(window=60).mean()

# # 이동평균선 5분 기준 추가(window=고려일수)
# df['ma120'] = df['close'].rolling(window=120).mean()

# # 변동폭 * k 계산, (고가 - 저가) * k값 - 삭제처리
# df['range'] = (df['high'] - df['low']) * 0.5

# # target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
# df['target'] = df['open'] + df['range'].shift(1)

# # bull = 전일종가 > 이평선보다 높을경우 TRUE
# df['bull'] = df['open'] > df['ma5']

# # bull = 이평선20 * 가중치 - 횡보장 거래 정지선
# df['bull'] = df['ma20'] * 1.05

# # ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
# fee = 0.0005
# df['ror'] = np.where((df['ma5'] > df['ma10']) & (df['ma5'] > df['bull']), # 이평선 이상일 경우 값 추출 추가 MA버전 삽입분
#                       df['close'] / df['close'].shift(1) - fee,
#                       1)

# # 누적 곱 계산(cumprod) => 누적 수익률
# df['hpr'] = df['ror'].cumprod()

# # Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
# df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

# #MDD 계산
# print("MDD: ", df['dd'].max())

# #HPR 계산 (기간수익율)
# print("HPR: ", df['hpr'][-2])

#엑셀로 출력
df.to_excel("minute_ma.xlsx")
print("OK")