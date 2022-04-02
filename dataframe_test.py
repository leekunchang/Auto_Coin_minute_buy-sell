from cmath import e
from ctypes.wintypes import tagRECT
import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-SAND","minute60",24)
df['ma2'] = df['close'].ewm(2).mean()
df['ma2b'] = df['close'].ewm(2).mean().shift(1)
df['ma3'] = df['close'].ewm(3).mean()
df['ma3b'] = df['close'].ewm(3).mean().shift(1)
df['ma5'] = df['close'].ewm(5).mean()
df['ma5b'] = df['close'].ewm(5).mean().shift(1)
df['ma10'] = df['close'].ewm(10).mean()
df['low1'] = df['low'].iloc[-1]
df['open1'] = df['open'].iloc[-1] 
# df['ub/ma'] = np.where((df['high'] > df['ubc']) & (df['ma20a'] > df['close_a']) & (df['ma20b'] > df['close_b']) ,
#                     df['ubb'] / df['ma20'],
#                     10)



df.to_excel("111111.xlsx")