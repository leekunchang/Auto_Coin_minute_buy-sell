import pyupbit
import numpy as np

Coin_code = "FLOW" # 종목코드
K_code = 0.5 # K 값

# OHLCV(open, high, low, close, volume)로 당일 시가, 고가, 저가, 종가, 거래량에 대한 데이터
df = pyupbit.get_ohlcv("KRW-"+Coin_code, count=200)

# 이동평균선 3일기준 추가(window=고려일수)
df['ma5'] = df['close'].rolling(window=3).mean().shift(1)

# 변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * K_code

# target(매수가), range 컬럼을 한칸씩 밑으로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

# bull = 전일종가 > 이평선보다 높을경우 TRUE
df['bull'] = df['open'] > df['ma5']

# ror(수익률), np.where(조건문, 참일때 값, 거짓일때 값)
fee = 0.0005
df['ror'] = np.where((df['high'] > df['target']) & df['bull'], # 이평선 이상일 경우 값 추출 추가 MA버전 삽입분
                      df['close'] / df['target'] - fee,
                      1)

df['benefit'] = df['target'] * 1.0205 < df['high']

df['lose'] = df['ror'] < 1

# 누적 곱 계산(cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산 (누적 최대 값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100

#MDD 계산
print("MDD: ", df['dd'].max())

#HPR 계산 (기간수익율)
print("HPR: ", df['hpr'][-2])

#엑셀로 출력
df.to_excel("Backtest_day.xlsx")