import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

K_code = 0.5 # K 상수값
B_code = 1.0205 # 익절 희망 % - 수수료포함 2프로 먹고 타겟보다 1% 높을때 매수. (최소마진 1%)
coin_code = "WEMIX" # 종목코드


#수정전

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma3(ticker): # MA버전 추가분
    """3일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=3)
    ma3 = df['close'].rolling(3).mean().iloc[-1]
    return ma3

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
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-"+coin_code)
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-"+coin_code, K_code) # K상수값 K_code
            ma3 = get_ma3("KRW-"+coin_code) # MA버전 삽입분
            current_price = get_current_price("KRW-"+coin_code)
            benefit_price = target_price * B_code # 익절희망값(변수로지정됨)
            # 매수조건 - 목표가 and 이평선 < 현재가격 < 타겟가격 * 1.01 < 익절값
            # 실제 매수조건은 목표+이평선 도달 시 매수, 그리고 매수가보다 1% 높으면 안사짐. 조건에 합할 경우 수차례 사짐
            if target_price < current_price and ma3 < current_price and current_price < benefit_price and current_price < target_price * 1.01:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
            elif target_price < current_price and benefit_price < current_price: # 익절코드
                coin_volume = get_balance(coin_code)
                if coin_volume > 0.00008:
                    upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
        else:
            coin_volume = get_balance(coin_code)
            if coin_volume > 0.00008:
                upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
