import os.path
import json
import datetime

import tabulate

import mydatetime
import util


# 第1限月の残り週数をNとする。

# 期近売り相当 = PUT買い
# 第1限月 N枚
# 第2限月 (5-N)枚

# 期先買い相当 = CALL買い
# 第2限月 N枚
# 第3限月 (5-N)枚

PUT_DELTA_THRESHOLD = -0.8
CALL_DELTA_THRESHOLD = 0.8


def calendar():
    path = os.path.join("./data", "expirations.json")
    with open(path) as f:
        expirations = json.load(f)
    expirations = list(map(mydatetime.parse_date, expirations))
    (first, second) = util.split_first_second(expirations[0], 5)
    print("PUT to buy")
    buy_put(expirations, first, second)
    print()
    print("CALL to buy")
    buy_call(expirations, first, second)


def buy_put(expirations: list[datetime.datetime], first: int, second: int) -> None:
    table = list()
    table.append((1, mydatetime.format_date(expirations[0]), first))
    table.append((2, mydatetime.format_date(expirations[1]), second))
    print(tabulate.tabulate(table, headers=("Month", "Expire date", "Quantity")))
    print()
    put_to_buy(expirations[1])


def put_to_buy(expiration: datetime.datetime) -> None:
    dir_path = os.path.join("./data", expiration.strftime("%Y%m%d"))
    path = os.path.join(dir_path, "put.json")
    with open(path) as f:
        records = json.load(f)
    for record in records:
        delta = record["delta"]
        if delta is None:
            continue
        if record["delta"] < PUT_DELTA_THRESHOLD:
            print("Expire at: ", mydatetime.format_date(expiration))
            print("Strike price: ", record["strike"])
            print("Delta: ", delta)
            return


def buy_call(expirations: list[datetime.datetime], first: int, second: int) -> None:
    table = list()
    table.append((2, mydatetime.format_date(expirations[1]), first))
    table.append((3, mydatetime.format_date(expirations[2]), second))
    print(tabulate.tabulate(table, headers=("Month", "Expire date", "Quantity")))
    print()
    call_to_buy(expirations[2])


def call_to_buy(expiration: datetime.datetime) -> None:
    dir_path = os.path.join("./data", expiration.strftime("%Y%m%d"))
    path = os.path.join(dir_path, "call.json")
    with open(path) as f:
        records = json.load(f)
    for record in reversed(records):
        delta = record["delta"]
        if delta is None:
            continue
        if record["delta"] > CALL_DELTA_THRESHOLD:
            print("Expire at: ", mydatetime.format_date(expiration))
            print("Strike price: ", record["strike"])
            print("Delta: ", delta)
            return
