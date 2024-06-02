import json
import os.path
import datetime

import tabulate

# 第6限月のPUTを購入し、満期まで保有する。
# Delta -0.8を目安としPUTを購入する。


DELTA_THRESHOLD = -0.8


def sixmonth():
    path = os.path.join("./data", "expirations.json")
    with open(path) as f:
        expirations = json.load(f)
    list_expirations(expirations)
    print()
    buy_put(expirations[5])


def list_expirations(expirations: list[str]) -> None:
    table = list()
    for i in range(6):
        date = format_expiration(expirations[i])
        table.append((i + 1, date))
    print(tabulate.tabulate(table, headers=("Month", "Expire date")))


def buy_put(expiration: str) -> None:
    dir_path = os.path.join("./data", expiration)
    path = os.path.join(dir_path, "put.json")
    with open(path) as f:
        records = json.load(f)
    for record in records:
        delta = record["delta"]
        if delta is None:
            continue
        if record["delta"] < DELTA_THRESHOLD:
            date = format_expiration(expiration)
            print("PUT to buy")
            print("Expire at: ", date)
            print("Strike price: ", record["strike"])
            print("Delta: ", delta)
            return


def format_expiration(expiration: str) -> str:
    return datetime.datetime.strptime(expiration, "%Y%m%d").strftime("%Y/%m/%d")
