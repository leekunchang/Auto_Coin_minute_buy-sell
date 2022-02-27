from cmath import e
from ctypes.wintypes import tagRECT
import pyupbit
import numpy as np

def get_ub_ma_a(ticker):
    df = pyupbit.get_ohlcv(ticker,"minute60",24)
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    df['dbb'] = df['ma20'] - 2 * df['close'].rolling(window=20).std()
    df['ubc'] = (df['ubb'] + df['ma20']) / 2
    df['close_a'] = df['close'].shift(1)
    df['close_b'] = df['close'].shift(2)
    df['ma20a'] = df['ma20'].shift(1)
    df['ma20b'] = df['ma20'].shift(2)
    df['ub/ma'] = np.where((df['high'] > df['ubc']) & (df['ma20a'] > df['close_a']) & (df['ma20b'] > df['close_b']) ,
                    df['ubb'] / df['ma20'],
                    10)
    return df['ub/ma']

def get_ub_ma_b(ticker):
    df = pyupbit.get_ohlcv(ticker,"minute60",24)
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    df['dbb'] = df['ma20'] - 2 * df['close'].rolling(window=20).std()
    df['ubc'] = (df['ubb'] + df['ma20']) / 2
    df['close_a'] = df['close'].shift(1)
    df['close_b'] = df['close'].shift(2)
    df['ma20a'] = df['ma20'].shift(1)
    df['ma20b'] = df['ma20'].shift(2)
    df['ub/ma'] = np.where((df['high'] > df['ubc']),
                    df['ubb'] / df['ma20'],
                    10)
    return df['ub/ma']

def get_ub_ma_c(ticker):
    df = pyupbit.get_ohlcv(ticker,"minute60",24)
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    df['dbb'] = df['ma20'] - 2 * df['close'].rolling(window=20).std()
    df['ubc'] = (df['ubb'] + df['ma20']) / 2
    df['close_a'] = df['close'].shift(1)
    df['close_b'] = df['close'].shift(2)
    df['ma20a'] = df['ma20'].shift(1)
    df['ma20b'] = df['ma20'].shift(2)
    df['ub/ma'] = df['ubb'] / df['ma20']

    return df['ub/ma']

tickers = pyupbit.get_tickers(fiat="KRW")

print("볼린저랑 ma20 중간값이상 + 전전봉 종가는 ma20미만")
ub_ma_a = []
playtime = 0
while playtime < 30:
  playtime = playtime + 1
  try:
    for ticker in tickers:
      lisst_a = get_ub_ma_a(ticker).iloc[-1]
      ub_ma_a.append((ticker, lisst_a))
  except:
    pass

# print(ub_ma)
sorted_ub_ma_a = sorted(ub_ma_a, key=lambda x:x[1])
print(sorted_ub_ma_a)
print("--------------")
print("--------------")


print("볼린저랑 ma20 중간값이상")
ub_ma_b = []
playtime = 0
while playtime < 30:
  playtime = playtime + 1
  try:
    for ticker in tickers:
      lisst_b = get_ub_ma_b(ticker).iloc[-1]
      ub_ma_b.append((ticker, lisst_b))
  except:
    pass

# print(ub_ma)
sorted_ub_ma_b = sorted(ub_ma_b, key=lambda x:x[1])
print(sorted_ub_ma_b)
print("--------------")
print("--------------")


print("볼린저 폭으로 오름차순")
ub_ma_c = []
playtime = 0
while playtime < 30:
  playtime = playtime + 1
  try:
    for ticker in tickers:
      lisst_c = get_ub_ma_c(ticker).iloc[-1]
      ub_ma_c.append((ticker, lisst_c))
  except:
    pass

# print(ub_ma)
sorted_ub_ma_c = sorted(ub_ma_c, key=lambda x:x[1])
print(sorted_ub_ma_c)

print("출력완료")