import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

coin_code = "JST" # 종목코드


def get_ma5(ticker): # 분봉 22분 조회, 5분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma5 = df['close'].rolling(5).mean()
    return ma5

def get_ma10(ticker): # 분봉 22, 조회 10분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma10 = df['close'].rolling(10).mean()
    return ma10

def get_ma20(ticker): # 분봉 22, 조회 20분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=22)
    ma20 = df['close'].rolling(20).mean()
    return ma20

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        ma5 = get_ma5("KRW-"+coin_code) # ma5 값 차트 불러오는 함수
        ma10 = get_ma10("KRW-"+coin_code) # ma10 값 차트 불러오는 함수
        ma20 = get_ma20("KRW-"+coin_code) # ma20 값 차트 불러오는 함수
        # 매수조건 - 목표가 and 이평선 < 현재가격 < 타겟가격 * 1.01 < 익절값
        # 실제 매수조건은 목표+이평선 도달 시 매수, 그리고 매수가보다 1% 높으면 안사짐. 조건에 합할 경우 수차례 사짐
        if ma10 < ma5 and ma20 * 1.05 < ma5:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
        else:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
