import time
import pyupbit
import datetime

coin_code = "MBL" 

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]


playtime = 0
lisst = []
while True:
    try:
        now = datetime.datetime.now()
        if now.second < 2 :
            current_price = get_current_price("KRW-"+coin_code)
            # print(current_price)
            lisst.append(current_price)
            print(lisst, coin_code)
            min_lisst = min(lisst)
            print(min_lisst)

    except Exception as e:
        print(e)
        time.sleep(1)