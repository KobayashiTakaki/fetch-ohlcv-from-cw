from os import path
from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin
import json
import requests

BASE_URL = 'https://api.cryptowat.ch/'
OHLC_PATH = 'markets/bitflyer/btcfxjpy/ohlc'
TZ_JST = timezone(timedelta(hours=9))
PERIODS = 300
FETCH_CHUNK_PERIOD = timedelta(days=7)

def main():
    config = get_config()
    output_path = config["output_path"]
    time_from = config["time_from"]
    time_to = config["time_to"]
    time_from_current = time_from
    time_to_current = time_from_current + FETCH_CHUNK_PERIOD

    while time_to_current < time_to + FETCH_CHUNK_PERIOD:
        if time_to_current + FETCH_CHUNK_PERIOD > time_to:
            time_to_current = time_to
        params = {
            "periods": PERIODS,
            "after": int(time_from_current.timestamp()),
            "before": int(time_to_current.timestamp()),
        }
        print("fetch ohlcv, time_from: {}, time_to: {}".format(time_from_current, time_to_current))
        res = requests.get(urljoin(BASE_URL, OHLC_PATH), params=params)
        res_json = json.loads(res.content)
        print("cost: ", res_json["allowance"]["cost"])
        print("remaining: ", res_json["allowance"]["remaining"])
        candles = res_json["result"][str(PERIODS)]
        with open(output_path, mode='a') as f:
            for candle in candles:
                f.write(str(candle[0]))
                f.write(',')
                f.write(str(candle[1]))
                f.write(',')
                f.write(str(candle[2]))
                f.write(',')
                f.write(str(candle[3]))
                f.write(',')
                f.write(str(candle[4]))
                f.write(',')
                f.write(str(candle[5]))
                f.write('\n')
        time_from_current = time_to_current
        time_to_current = time_to_current + FETCH_CHUNK_PERIOD

def get_config():
    output_path = path.join(path.dirname(__file__), 'tmp', 'candles.csv')
    time_from = datetime(2022, 1, 1, 0, 0, 0, 0, TZ_JST)
    time_to = datetime.now(TZ_JST)
    return {
        "output_path": output_path,
        "time_from": time_from,
        "time_to": time_to,
    }

if __name__ == "__main__":
    main()
