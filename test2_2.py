from cmath import e
from ctypes.wintypes import tagRECT
import pyupbit
import numpy as np

def get_ub_ma(ticker):
    df = pyupbit.get_ohlcv(ticker,"minute60",21)
    df['ma20'] = df['close'].rolling(window=20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    df['dbb'] = df['ma20'] - 2 * df['close'].rolling(window=20).std()
    df['ub/ma'] = np.where((df['high'] > df['ubb']),
                      df['ubb'] / df['ma20'],
                      10)
    return df['ub/ma']


lisst = get_ub_ma("KRW-LTC").iloc[-1]
print(lisst)