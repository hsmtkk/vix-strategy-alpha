import ib_insync as ib
import os.path
import json

SYMBOL_VIX = "VIX"
EXCHANGE_CBOE = "CBOE"
RIGHT_CALL = "C"
RIGHT_PUT = "P"

# https://interactivebrokers.github.io/tws-api/market_data_type.html
MARKET_DATA_TYPE_DELAYED = 4


def download():
    ib.util.startLoop()
    broker = ib.IB()
    broker.connect(readonly=True)
    broker.reqMarketDataType(MARKET_DATA_TYPE_DELAYED)

    chain = vix_cboe_monthly(broker)
    # print(chain)

    save_expirations(chain.expirations)

    for expiration in chain.expirations:
        call_ticks = option_ticks(broker, expiration, chain.strikes, RIGHT_CALL)
        save_ticks(expiration, RIGHT_CALL, call_ticks)
        put_ticks = option_ticks(broker, expiration, chain.strikes, RIGHT_PUT)
        save_ticks(expiration, RIGHT_PUT, put_ticks)


def vix_cboe_monthly(broker: ib.IB) -> ib.OptionChain:
    vix = ib.Index(SYMBOL_VIX, EXCHANGE_CBOE)
    broker.qualifyContracts(vix)
    chains = broker.reqSecDefOptParams(vix.symbol, "", vix.secType, vix.conId)
    for chain in chains:
        if chain.exchange == EXCHANGE_CBOE and chain.tradingClass == SYMBOL_VIX:
            return chain
    raise Exception("Not found")


def save_expirations(expirations: list[str]) -> None:
    path = os.path.join("./data", "expirations.json")
    with open(path, "w") as f:
        f.write(json.dumps(expirations))


def option_ticks(
    broker: ib.IB, expire: str, strikes: list[float], right: str
) -> list[ib.Ticker]:
    opts = list()
    for strike in strikes:
        opt = ib.Option(
            symbol=SYMBOL_VIX,
            lastTradeDateOrContractMonth=expire,
            strike=strike,
            right=right,
            exchange=EXCHANGE_CBOE,
        )
        broker.qualifyContracts(opt)
        opts.append(opt)
    return broker.reqTickers(*opts)


def save_ticks(expiration: str, right: str, tickers: list[ib.Ticker]) -> None:
    dir_path = os.path.join("./data", expiration)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if right == RIGHT_CALL:
        file_name = "call.json"
    else:
        file_name = "put.json"
    path = os.path.join(dir_path, file_name)
    records = list()
    for tick in tickers:
        delta = 0
        if tick.modelGreeks is not None:
            delta = tick.modelGreeks.delta
        record = {
            "strike": tick.contract.strike,
            "last": tick.last,
            "delta": delta,
        }
        records.append(record)
    with open(path, "w") as f:
        f.write(json.dumps(records))
