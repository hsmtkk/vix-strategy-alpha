import os
import json
import datetime

import tabulate

# 第1限月の残り週数をNとする。

# VXX売り相当 = PUT買い
# Delta -0.8を目安とする。
# 第1限月の残り週数をNとする。
# 第1限月 N枚
# 第2限月 (5-N)枚

# VXZ買い相当 = CALL買い
# 第3，4，5，6，7限月 各1枚
# Delta 0.8を目安とする。

PUT_DELTA_THRESHOLD = -0.8
CALL_DELTA_THRESHOLD = 0.8


def vxxvxz():
    path = os.path.join("./data", "expirations.json")
    with open(path) as f:
        expirations = json.load(f)
    expirations = list(map(parse_date, expirations))
    print("PUT to buy")
    buy_put(expirations)
    print()
    print("CALL to buy")
    buy_call(expirations)


def buy_put(expirations: list[datetime.datetime]) -> None:
    days_till_first_expiration = (expirations[0] - datetime.datetime.now()).days
    first_quantity = days_till_first_expiration // 7
    second_quantity = 5 - first_quantity
    table = list()
    table.append((1, format_date(expirations[0]), first_quantity))
    table.append((2, format_date(expirations[1]), second_quantity))
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
            print("Expire at: ", format_date(expiration))
            print("Strike price: ", record["strike"])
            print("Delta: ", delta)
            return


def buy_call(expirations: list[datetime.datetime]) -> None:
    table = list()
    for i in range(2, 7):
        table.append((i + 1, format_date(expirations[i]), 1))
    print(tabulate.tabulate(table, headers=("Month", "Expire date", "Quantity")))
    print()
    call_to_buy(expirations[6])


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
            print("Expire at: ", format_date(expiration))
            print("Strike price: ", record["strike"])
            print("Delta: ", delta)
            return


def parse_date(date: str) -> datetime.datetime:
    parsed = datetime.datetime.strptime(date, "%Y%m%d")
    return parsed


def format_date(date: datetime.datetime) -> str:
    return date.strftime("%Y/%m/%d")
