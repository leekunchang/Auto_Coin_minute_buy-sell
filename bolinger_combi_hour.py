from fileinput import close
import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

# 종목코드
coin_code = "SAND" 

def get_ma5(ticker): # 60분봉 23 조회, 5시간 단순이평, 5시간 표준편차 기준선
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma5a(ticker): # 60분봉 23 조회, 5시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma5a = df['close'].ewm(5).mean().iloc[-1] 
    return ma5a

def get_ma5b(ticker): # 60분봉 23 조회, 5시간 지수이평 전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma5b = df['close'].ewm(5).mean().iloc[-2] 
    return ma5b

def get_ma10a(ticker): # 60분봉 12, 10시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma10a = df['close'].ewm(10).mean().iloc[-1] 
    return ma10a

def get_ma10b(ticker): # 60분봉 12, 10시간 지수이평 전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma10b = df['close'].ewm(10).mean().iloc[-2] 
    return ma10b    

def get_close0(ticker): # 60분봉 23, 현종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    close0 = df['close'].iloc[-1] 
    return close0

def get_close1(ticker): # 60분봉 23, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    close1 = df['close'].iloc[-2] 
    return close1

def get_low0(ticker): # 60분봉 23, 현저가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    low0 = df['low'].iloc[-1] 
    return low0

def get_high0(ticker): # 60분봉 23, 현고가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    high0 = df['high'].iloc[-1] 
    return high0

def get_ubb(ticker): # 볼린저밴드 상단(내림에 대한 변수 대응으로 0.9995 곱함)
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma20'] = df['close'].rolling(20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    ubb = df['ubb'].iloc[-1] * 0.9995
    return ubb    

def get_dev_up(ticker): # 5시간 표준편차 상단가격
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma5'] = df['close'].rolling(5).mean()
    df['dev_up'] = df['ma5'] + 2 * df['close'].rolling(window=5).std()
    dev_up = df['dev_up'].iloc[-1] * 0.9995
    return dev_up

def get_dev_down(ticker): # 5시간 표준편차 하단가격
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma5'] = df['close'].rolling(5).mean()
    df['dev_down'] = df['ma5'] - 2 * df['close'].rolling(window=5).std()
    dev_down = df['dev_down'].iloc[-1] * 0.9995
    return dev_down

def get_current_price(ticker): # 현재가
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

def get_balance(ticker): # 잔고조회
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
        now = datetime.datetime.now() # 시간값
        current_price = get_current_price("KRW-"+coin_code) # 현재가
        now = datetime.datetime.now() # 시간값
        current_price = get_current_price("KRW-"+coin_code) # 현재가
        ma5 = get_ma5("KRW-"+coin_code) # 5시간 편차의 기준값
        ma5a = get_ma5a("KRW-"+coin_code) # 5시간 지수이평
        ma5b = get_ma5b("KRW-"+coin_code) # 5시간 지수이평 전봉
        ma10a = get_ma10a("KRW-"+coin_code) # 10시간 지수이평
        ma10b = get_ma10b("KRW-"+coin_code) # 10시간 지수이평 전봉
        close0 = get_close0("KRW-"+coin_code) # 현종가
        close1 = get_close1("KRW-"+coin_code) # 전종가
        low0 = get_low0("KRW-"+coin_code) # 현저가
        high0 = get_high0("KRW-"+coin_code) # 현고가
        ubb = get_ubb("KRW-"+coin_code) # 볼린저밴드 상단
        div_high = high0 - close0 # 상단 - 종가. 위쪽 꼬리 가격
        div_low = close1 - low0  # 하단 - 전종가. 아래쪽 꼬리 가격
        dev_up = get_dev_up("KRW-"+coin_code) # 5시간 표준편차 상단가격
        dev_down = get_dev_down("KRW-"+coin_code) # 5시간 표준편차 하단가격
        dev_div_up = dev_up / ma5 # 표준편차의 넓이값 상단
        dev_div_down = dev_down / ma5 # 표준편차의 넓이값 하단
        dodge_up = (dev_up - ma5) * 0.3 # 위쪽 꼬리 편차의 30% 길이를 곱한 값
        dodge_down = (ma5 - dev_down) * 0.3 # 아래쪽 꼬리 편차의 30% 길이를 곱한 값
        sell_price = 1 - (ma5 / dev_down -1 ) * 3 # 아래로 표준편차의 3배값만큼 하락한 값

        if now.minute < 2 :
            print("모니터링. 매수가 : ", lisst[0])

        if 57 < now.minute :
            if ma5a > ma5b and ma10a > ma10b and ma5a > ma10a and div_high < dodge_up and div_low < dodge_down and high0 < ubb  and dev_div_up > 1.006 :
                krw = get_balance("KRW") # 5이평 상승 and 10이평 상승 and 윗꼬리는 편차0.3이내 and 아래꼬리는 편차0.3이내 and 밴드상단 조건 and 밴드폭 조건(익절0.6가능한지)
                if krw > 5000:
                    upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
                    lisst.append(current_price)
                    min_lisst = lisst[0]
                    print("매수")
                    print("매수가", min_lisst, "리스트", lisst)
                # time.sleep(30) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)

        if min_lisst * dev_div_up < current_price: # 편차만큼 상승하면 익절
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("익절")
                print("매수가 : ", min_lisst, "매도가 : ", current_price, "이론상판매가 : ", min_lisst * 1.011)
                lisst = []
                # time.sleep(3600) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)
                
            time.sleep(1)

    
            

        if min_lisst * sell_price > current_price or min_lisst * 0.92 > current_price : # 아래편차 3배 혹은 8%이하로 내려가면 손절
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