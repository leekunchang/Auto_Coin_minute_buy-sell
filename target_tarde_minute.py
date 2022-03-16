from fileinput import close
import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

# 종목코드
coin_code = "WAVES" 


def get_ma5a(ticker): # 분봉 12분 조회, 5시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=12)
    ma5a = df['close'].ewm(5).mean().iloc[-1] 
    return ma5a

def get_ma5b(ticker): # 분봉 12분 조회, 5시간 지수이평 전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=12)
    ma5b = df['close'].ewm(5).mean().iloc[-2] 
    return ma5b

def get_ma5c(ticker): # 분봉 12분 조회, 5시간 지수이평 전전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=12)
    ma5c = df['close'].ewm(5).mean().iloc[-3] 
    return ma5c

def get_ma10(ticker): # 분봉 12, 10시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=12)
    ma10 = df['close'].ewm(10).mean().iloc[-1] 
    return ma10

def get_close1(ticker): # 분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=12)
    close1 = df['close'].iloc[-2] 
    return close1

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

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

lisst = []

while True:
    try:
        ma5a = get_ma5a("KRW-"+coin_code) # ma5 값 차트 불러오는 함수
        ma5b = get_ma5b("KRW-"+coin_code) # 1시간전 ma5 차트 불러오는 함수
        ma5c = get_ma5c("KRW-"+coin_code) # 2시간전 ma5 차트 불러오는 함수
        ma10 = get_ma10("KRW-"+coin_code) # ma10 값 차트 불러오는 함수
        current_price = get_current_price("KRW-"+coin_code)
        close1 = get_close1("KRW-"+coin_code) # ma5 값 차트 불러오는 함수

        if ma5a > ma5b and ma5a > ma10:
            lisst.append(current_price)
            min_lisst = min(lisst)
            print(min_lisst)                
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
                print("매수")
                time.sleep(30) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)

        if min_lisst * 1.011 < current_price:
            print("매수가 : ", min_lisst, "매도가 : ", current_price)
            lisst = []
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("익절")
                time.sleep(30) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)
                
            time.sleep(1)

    
            

        if min_lisst * 0.97 < current_price :
            coin_volume = get_balance(coin_code)
            print("매수가 : ", min_lisst, "매도가 : ", current_price)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("손절")

    except Exception as e:
        print(e)
        time.sleep(1)



# asyncio 비동기