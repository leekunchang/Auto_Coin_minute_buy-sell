import time

ddd = 0

while ddd < 8:
    print(ddd)
    ddd = ddd + 1
    if ddd > 3:
        print("기준1")
        break
    if ddd > 5:
        print("기준2")
    time.sleep(0.1)