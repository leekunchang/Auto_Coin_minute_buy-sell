from ctypes.wintypes import tagRECT
import pyupbit
import numpy as np
import math
import pandas as pd

print
# df = pyupbit.get_ohlcv("KRW-ONG","day",30)
# df['ma20'] = df['close'].rolling(window=20).mean()
# df['stddev'] = df['close'].rolling(window=20).std()
# df['ubb'] = df['ma20'] + 2 * df['stddev']
# df['dbb'] = df['ma20'] - 2 * df['stddev']
# df['ub/ma'] = np.where((df['high'] > df['ubb']),
#                     df['ubb'] / df['ma20'],
#                     10)
#                     #   .iloc[-1]
def get_ub_ma(ticker):
    df = pyupbit.get_ohlcv(ticker,"minute60",60)
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    df['dbb'] = df['ma20'] - 2 * df['close'].rolling(window=20).std()
    df['ub/ma'] = np.where((df['high'] > df['ubb']), df['ubb'] / df['ma20'], 10)
                    #   .iloc[-1]
    return df['ub/ma']
ub_ma = get_ub_ma("KRW-ONG")
print(ub_ma)

# ub_ma.to_excel("lissst.xlsx")