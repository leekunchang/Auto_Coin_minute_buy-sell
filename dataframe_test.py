from cmath import e
from ctypes.wintypes import tagRECT
import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-MTL","minute60",24)
# df['ma20'] = df['close'].rolling(window=20).mean()
# df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
# df['dbb'] = df['ma20'] - 2 * df['close'].rolling(window=20).std()
# df['ubc'] = (df['ubb'] + df['ma20']) / 2
# df['close_a'] = df['close'].shift(1)
# df['close_b'] = df['close'].shift(2)
# df['ma20a'] = df['ma20'].shift(1)
# df['ma20b'] = df['ma20'].shift(2)
df['ma5a'] = df['close'].rolling(window=5).mean()
df['ma5b'] = df['close'].rolling(window=5).mean().shift(1)
df['ma10'] = df['close'].rolling(window=10).mean()
# df['ub/ma'] = np.where((df['high'] > df['ubc']) & (df['ma20a'] > df['close_a']) & (df['ma20b'] > df['close_b']) ,
#                     df['ubb'] / df['ma20'],
#                     10)



df.to_excel("hansang2.xlsx")