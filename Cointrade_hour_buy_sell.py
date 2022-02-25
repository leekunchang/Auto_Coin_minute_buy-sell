import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

coin_code = "MATIC" # 종목코드


def get_ma5a(ticker): # 60분봉 12분 조회, 5분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma5a = df['close'].rolling(5).mean().iloc[-1] # 현재 5시간 이평선 조회(-1)
    return ma5a

def get_ma5b(ticker): # 60분봉 12분 조회, 5분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma5b = df['close'].rolling(5).mean().iloc[-2] # 전 5시간 이평선 조회(-2)
    return ma5b

def get_ma5c(ticker): # 60분봉 12분 조회, 5분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma5c = df['close'].rolling(5).mean().iloc[-3] # 전전 5시간 이평선 조회(-3)
    return ma5c

def get_ma10(ticker): # 60분봉 12, 조회 10분 이평선
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma10 = df['close'].rolling(10).mean().iloc[-1] # 현재 10시간 이평선
    return ma10


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


# 현재가 조회 보류상태
# def get_current_price(ticker):
#     """현재가 조회"""
#     return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        ma5a = get_ma5a("KRW-"+coin_code) # ma5 값 차트 불러오는 함수
        ma5b = get_ma5b("KRW-"+coin_code) # 1시간전 ma5 차트 불러오는 함수
        ma5c = get_ma5c("KRW-"+coin_code) # 2시간전 ma5 차트 불러오는 함수
        ma10 = get_ma10("KRW-"+coin_code) # ma10 값 차트 불러오는 함수
        
        if ma5a > ma5b and ma5a > ma10:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
                print("매수")
                time.sleep(1800) # 매수 후 30분간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)
                
        if ma5a < ma5b or ma5a < ma10:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("매도")
                time.sleep(1800) # 매수 후 30분간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)
                
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)