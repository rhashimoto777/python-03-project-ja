import fetch_data
import pandas as pd
import sqlite3
from sqlite3 import Error

# Local実行モード（サーバーからAPIでデータ取得せず，Local上のDumpからデータ取得する．API呼び出し回数を消費しないためのモード）
IS_LOCAL_MODE = False

# APIキー
openweather_api_key = '71a673e4a77aa9bdc2e8a53467d75a82'
news_api_key = '5d07dbd3bf274e6dae1030b52f4b8f1a'

cities = []
cities.append({"jp":"東京", "en":"Tokyo"})
cities.append({"jp":"京都", "en":"Kyoto"})
cities.append({"jp":"大阪", "en":"Osaka"})
cities.append({"jp":"福岡", "en":"Fukuoka"})
cities.append({"jp":"札幌", "en":"Sapporo"})

def add_city_id():
    for i, elem in enumerate(cities):
        elem["city_id"] = i
    return


def main():
    add_city_id()

    # データを取得し，DataFrameに変換
    weather_data = fetch_data.WeatherData(openweather_api_key, IS_LOCAL_MODE)
    weather_df = weather_data.make_df(cities)
    print("------ debug : weather_df ------")
    print(weather_df)

    # news_data = fetch_data.NewsData(news_api_key, IS_LOCAL_MODE)
    # news_df = news_data.make_df(cities)
    # print("------ debug : news_df ------")
    # print(news_df)

    # SQLデータベースに統合
    # TBD．別の.pyファイルに分割しで計算する．
    # 長越さん

    # 表示
    # TBD．別の.pyファイルに分割しで計算する．
if __name__ == "__main__":
    main()