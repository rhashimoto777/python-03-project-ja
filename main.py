import fetch_data
import pandas as pd
import sqlite3

#________________________________________________________________________________________________________________________
# Local実行モード（サーバーからAPIでデータ取得せず，Local上のDumpからデータ取得する．API呼び出し回数を消費しないためのモード）
IS_LOCAL_MODE = True
# デバッグ用のprintを表示するモード
IS_DEBUG_PRINT_MODE = True

#________________________________________________________________________________________________________________________
# APIキー
openweather_api_key = '71a673e4a77aa9bdc2e8a53467d75a82'
news_api_key = '5d07dbd3bf274e6dae1030b52f4b8f1a'

#________________________________________________________________________________________________________________________
# 対象都市
cities = []
cities.append({"jp":"東京", "en":"Tokyo"})
cities.append({"jp":"京都", "en":"Kyoto"})
cities.append({"jp":"大阪", "en":"Osaka"})
cities.append({"jp":"福岡", "en":"Fukuoka"})
cities.append({"jp":"札幌", "en":"Sapporo"})

#________________________________________________________________________________________________________________________
def add_city_id():
    """
    city_idは都市ごとにuniqueであれば何でも良いので，citiesのindexをIDとして用いる。
    IDが自動で採番されることと合わせて、これらによりIDの唯一性を担保する。
    """
    for i, elem in enumerate(cities):
        elem["city_id"] = i
    return
    
def main():
    # \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ 
    # 【1】データを取得し，DataFrameに変換
    # \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ 

    # 「city_name」に相当するDataFrame
    add_city_id()
    city_df =  pd.DataFrame(cities)

    # 「weather_current」に相当するDataFrame
    weather_data = fetch_data.WeatherData(openweather_api_key, IS_LOCAL_MODE)
    weather_df = weather_data.make_df(cities)
    if IS_DEBUG_PRINT_MODE:
        weather_data.print_df_for_debug(weather_df)

    # 「news_latest」に相当するDataFrame
    news_data = fetch_data.NewsData(news_api_key, IS_LOCAL_MODE)
    news_df = news_data.make_df(cities)
    if IS_DEBUG_PRINT_MODE:
        news_data.print_df_for_debug(news_df)

    # \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ 
    # 【2】SQLデータベースに統合
    # \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ 
    # TBD．別の.pyファイルに分割しで計算する．
    # 長越さん

    # \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ 
    # 【3】表示
    # \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ \__ 
    # TBD．別の.pyファイルに分割しで計算する．

#________________________________________________________________________________________________________________________
if __name__ == "__main__":
    main()