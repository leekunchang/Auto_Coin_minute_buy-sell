from fileinput import close
import time
import pyupbit
import datetime

access = "K1izlIYmgptIBMaMhfaZlWh8KlFnUXOxIXmS91pA"
secret = "x4vnFWp8mViKuunhEZwkAaojIomtTNnzVx6xMIDi"

# 종목코드
coin_code = "SAND" 

def get_ma5(ticker): # 60분봉 12분 조회, 5시간 단순이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma5a(ticker): # 60분봉 12분 조회, 5시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma5a = df['close'].ewm(5).mean().iloc[-1] 
    return ma5a

def get_ma5b(ticker): # 60분봉 12분 조회, 5시간 지수이평 전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma5b = df['close'].ewm(5).mean().iloc[-2] 
    return ma5b

def get_ma5c(ticker): # 60분봉 12분 조회, 5시간 지수이평 전전봉
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma5c = df['close'].ewm(5).mean().iloc[-3] 
    return ma5c

def get_ma10a(ticker): # 60분봉 12, 10시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma10a = df['close'].ewm(10).mean().iloc[-1] 
    return ma10a

def get_ma10b(ticker): # 60분봉 12, 10시간 지수이평
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    ma10b = df['close'].ewm(10).mean().iloc[-2] 
    return ma10b

def get_close0(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    close0 = df['close'].iloc[-1] 
    return close0

def get_close1(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    close1 = df['close'].iloc[-2] 
    return close1

def get_low1(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    low1 = df['low'].iloc[-1] 
    return low1

def get_high1(ticker): # 60분봉 12, 전종가
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    high1 = df['high'].iloc[-1] 
    return high1

def get_ubb(ticker): 
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma20'] = df['close'].rolling(20).mean()
    df['ubb'] = df['ma20'] + 2 * df['close'].rolling(window=20).std()
    ubb = df['ubb'].iloc[-1]
    return ubb    

def get_dev_up(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma5'] = df['close'].rolling(5).mean()
    df['dev_up'] = df['ma5'] + 2 * df['close'].rolling(window=5).std()
    dev_up = df['dev_up'].iloc[-1] * 0.9995
    return dev_up

def get_dev_down(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute60", count=23)
    df['ma5'] = df['close'].rolling(5).mean()
    df['dev_down'] = df['ma5'] - 2 * df['close'].rolling(window=5).std()
    dev_down = df['dev_down'].iloc[-1] * 0.9995
    return dev_down

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

ma5 = get_ma5("KRW-"+coin_code) 
ma5a = get_ma5a("KRW-"+coin_code) 
ma5b = get_ma5b("KRW-"+coin_code) 
ma10a = get_ma10a("KRW-"+coin_code) 
ma10b = get_ma10b("KRW-"+coin_code) 
close0 = get_close0("KRW-"+coin_code) #쓸일 없음
close1 = get_close1("KRW-"+coin_code) #쓸일 없음
low1 = get_low1("KRW-"+coin_code) #쓸일 없음
high1 = get_high1("KRW-"+coin_code) #쓸일 없음
ubb = get_ubb("KRW-"+coin_code) 
current_price = get_current_price("KRW-"+coin_code)
now = datetime.datetime.now()

low_close = low1 - close1 # 이거쓰며됨 
high_close = high1 - close0 # 이거쓰면됨
dev_up = get_dev_up("KRW-"+coin_code)
dev_down = get_dev_down("KRW-"+coin_code)
dev_div_up = dev_up / ma5
dev_div_down = dev_down / ma5
dodge_up = (dev_up - ma5) * 0.3 #상수값 입력예정 위쪽 꼬리 기준값 --------------꼭반영!!!
dodge_down = dev_div_down * 0.3 #상수값 입력예정 아래쪽 꼬리 기준값
target_up = dev_div_up * current_price
target_down = dev_div_down * current_price
sell_price = dev_div_down * 0.985

# low1/close1 high1/close0 high1 < ubb

print(dev_up, "5시간편차 상단 가격")
print(ma5, "편차 중심값")
print(dev_div_up, "5시간 편차 위로(0.9)")
print(dev_div_down, "5시간 편차 아래로(0.9)")
print(dodge_up, "위쪽 꼬리 기준")
print(high1 - close0, "고점-종가")
print(dodge_down, "아래쪽 꼬리 기준")
print(target_up, "익절희망 값")
print(target_down, "손절희망 값")
print(sell_price, "손절비율")

if high1 - close0 < dodge_up :
    print("위쪽 꼬리 짧음. 매수")
else :
    print("조건 미충족")

# while True:
#     try:
#         ma5a = get_ma5a("KRW-"+coin_code) 
#         ma5b = get_ma5b("KRW-"+coin_code) 
#         ma10a = get_ma10a("KRW-"+coin_code) 
#         ma10b = get_ma10b("KRW-"+coin_code) 
#         close0 = get_close0("KRW-"+coin_code) 
#         close1 = get_close1("KRW-"+coin_code) 
#         low1 = get_low1("KRW-"+coin_code)
#         high1 = get_high1("KRW-"+coin_code) 
#         ubb = get_ubb("KRW-"+coin_code) 
#         current_price = get_current_price("KRW-"+coin_code)
#         now = datetime.datetime.now()

#         if now.minute < 2 :
#             print("모니터링. 매수가 : ", lisst[0])

#         if 57 < now.minute :
#             if ma5a > ma5b and ma5a > ma10 and low1/close1 > 0.996 and high1/close0 < 1.007 and high1 < ubb * 0.9999:
#                 krw = get_balance("KRW")
#                 if krw > 5000:
#                     upbit.buy_market_order("KRW-"+coin_code, krw*0.9995)
#                     lisst.append(current_price)
#                     min_lisst = lisst[0]
#                     print("매수")
#                     print("매수가", min_lisst, "리스트", lisst)
#                 # time.sleep(30) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)

#         if min_lisst * 1.011 < current_price:
#             coin_volume = get_balance(coin_code)
#             if coin_volume > 0.00008:
#                 upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
#                 print("익절")
#                 print("매수가 : ", min_lisst, "매도가 : ", current_price, "이론상판매가 : ", min_lisst * 1.011)
#                 lisst = []
#                 # time.sleep(3600) # 매수 후 30초간 거래정지 (차트 등락에따른 불필요한 거래로 수수료손실 예방)
                
#             time.sleep(1)

    
            

#         if min_lisst * 0.97 > current_price :
#             coin_volume = get_balance(coin_code)
#             if coin_volume > 0.00008:
#                 upbit.sell_market_order("KRW-"+coin_code, coin_volume*0.9995)
#                 print("손절")
#                 print("매수가 : ", min_lisst, "매도가 : ", current_price, "이론상판매가 : ", min_lisst * 1.011)
#                 lisst = []
#                 # time.sleep(3600)

#     except Exception as e:
#         print(e)
#         time.sleep(1)



# # asyncio 비동기