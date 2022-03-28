from fileinput import close
import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

# 종목코드
coin_code = "SAND" 

def get_ma5a(ticker): # 60분봉 12분 조회, 5시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma5a = df['close'].ewm(5).mean().iloc[-1] 
    return ma5a

def get_ma5b(ticker): # 60분봉 12분 조회, 5시간 지수이평 전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma5b = df['close'].ewm(5).mean().iloc[-2] 
    return ma5b

def get_ma5c(ticker): # 60분봉 12분 조회, 5시간 지수이평 전전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma5c = df['close'].ewm(5).mean().iloc[-3] 
    return ma5c

def get_ma10(ticker): # 60분봉 12, 10시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    ma10 = df['close'].ewm(10).mean().iloc[-1] 
    return ma10

def get_close0(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    close0 = df['close'].iloc[-1] 
    return close0

def get_close1(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    close1 = df['close'].iloc[-2] 
    return close1

def get_low1(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    low1 = df['low'].iloc[-1] 
    return low1

def get_high1(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=12)
    high1 = df['high'].iloc[-1] 
    return high1

def get_ubb(ticker): 
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma20'] = df['close'].rolling(20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    ubb = df['ubb'].iloc[-1]
    return ubb    

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

now = datetime.datetime.now()

lisst = []
while True:
    try:    
        if now.second < 2 :
            print(lisst[0])
    except Exception as e:
        print(e)
        time.sleep(1)


while True:
    try:
        ma5a = get_ma5a("KRW-"+coin_code) 
        ma5b = get_ma5b("KRW-"+coin_code) 
        ma5c = get_ma5c("KRW-"+coin_code) 
        ma10 = get_ma10("KRW-"+coin_code) 
        current_price = get_current_price("KRW-"+coin_code)
        close0 = get_close0("KRW-"+coin_code) 
        close1 = get_close1("KRW-"+coin_code) 
        low1 = get_low1("KRW-"+coin_code)
        high1 = get_high1("KRW-"+coin_code) 
        ubb = get_ubb("KRW-"+coin_code) 
        now = datetime.datetime.now()
        if 57 < now.minute :
            if ma5a > ma5b and ma5a > ma10 and low1/close1 > 0.996 and high1/close0 < 1.007 and high1 < ubb * 0.9999:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
                    lisst.append(current_price)
                    min_lisst = lisst[0]
                    print("매수")
                    print("매수가", min_lisst, "리스트", lisst)
                # time.sleep(30) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)

        if min_lisst * 1.011 < current_price:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("익절")
                print("매수가 : ", min_lisst, "매도가 : ", current_price, "이론상판매가 : ", min_lisst * 1.011)
                lisst = []
                # time.sleep(3600) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)
                
            time.sleep(1)

    
            

        if min_lisst * 0.97 > current_price :
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("손절")
                print("매수가 : ", min_lisst, "매도가 : ", current_price, "이론상판매가 : ", min_lisst * 1.011)
                lisst = []
                # time.sleep(3600)

    except Exception as e:
        print(e)
        time.sleep(1)



# asyncio 비동기