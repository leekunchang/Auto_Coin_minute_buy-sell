from cmath import e
from ctypes.wintypes import tagRECT
import pyupbit
import numpy as np

def get_ub_ma(ticker):
    df = pyupbit.get_ohlcv(ticker,"minute60",21)
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    df['dbb'] = df['ma20'] - 2 * df['close'].rolling(window=20).std()
    df['ubc'] = (df['ubb'] + df['ma20']) / 2
    df['ub/ma'] = np.where((df['high'] > df['ubc']),
                      df['ubb'] / df['ma20'],
                      10)
    return df['ub/ma']

tickers = pyupbit.get_tickers()

ub_ma = []

playtime = 0
while playtime < 30:
  playtime = playtime + 1
  try:
    for ticker in tickers:
      lisst = get_ub_ma(ticker).iloc[-1]
      ub_ma.append((ticker, lisst))
  except:
    pass

# print(ub_ma)
sorted_ub_ma = sorted(ub_ma, key=lambda x:x[1])
print(sorted_ub_ma)