import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

# 종목코드
coin_code = "OMG" 


def get_ma20(ticker): 
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma20 = df['close'].rolling(20).mean().iloc[-1] 
    return ma20

def get_ubb(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma20'] = df['close'].rolling(20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    ubb = df['ubb'].iloc[-1]
    return ubb

def get_ubb_c(ticker): 
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma20'] = df['close'].rolling(20).mean() 
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std().iloc[-1]
    ubb_c = (df['ma20']+df['ubb']).iloc[-1] / 2
    return ubb_c

def get_benefit(ticker): 
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma20'] = df['close'].rolling(20).mean() 
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std().iloc[-1]
    df['ubb_c'] = (df['ma20']+df['ubb']) / 2
    ubb_benefit = (df['ubb_c']+df['ubb']).iloc[-1] / 2
    return ubb_benefit

def get_exit(ticker): 
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma20'] = df['close'].rolling(20).mean() 
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std().iloc[-1]
    df['ubb_c'] = (df['ma20']+df['ubb']) / 2
    ubb_exit = (df['ubb_c']+df['ma20']).iloc[-1] / 2
    return ubb_exit


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

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")


# 자동매매 시작
while True:
    try:
        ma20 = get_ma20("KRW-"+coin_code)
        ma_ubb = get_ubb("KRW-"+coin_code)
        ma_ubb_c = get_ubb_c("KRW-"+coin_code)
        ma_benefit = get_benefit("KRW-"+coin_code)
        ma_exit = get_exit("KRW-"+coin_code)
        current_price = get_current_price("KRW-"+coin_code)

        if ma_exit * 0.999 < current_price < ma_exit * 1.001:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
                print("매수")
                
                
        if ma_exit * 1.015 < current_price:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("익절")
                

        if current_price < ma20:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
                print("손절")
                

        if current_price < ma20 * 0.99:
            print("종료")
            break                
                
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)