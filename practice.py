import datetime

now = datetime.datetime.now()

print(now.second)

while True:
    now = datetime.datetime.now()
    if 50 < now.second < 60:
        print(now.second)