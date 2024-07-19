import pandas as pd
import sqlite3
import os

def display_data():
   """
   SQLiteデータベースからデータを読み込み、結合して表示する
   """
   # SQLiteデータベースからDataFrameを取得する。
   try:
      df_integrated = _gen_df_from_db()
   except Exception as e:
      print(f'Generating DataFrame from SQLite-DB failed : {e}')
      return

   # keyの一覧を表示
   print("\n######################## DataFrame gained from SQLite-DB file ########################")
   print("----------< Keys >----------\n")
   print(df_integrated.keys())

   # DataFrameの生データを表示。表示スペースの関係上一部データは省く。
   print("\n\n----------< DataFrame Raw Data (except news_2, news_3) >----------\n")
   print(df_integrated[['overview_id', 'date', 'city_id', 'weather_id', 'news_id', 'jp_name', 'en_name', 'weather', 'temperature', 'news_1']])
   
   # Dataの概要を見やすい形で表示
   datestr = get_time_from_df(df_integrated)
   if datestr:
      datestr = "at " + datestr + " "
   else:
      datestr = ""
   print(f'\n\n----------< Overview {datestr}>----------')

   for i in range(len(df_integrated)):
      elem = df_integrated.iloc[i]
      print(f'\n【{elem.loc["overview_id"]}】{elem.loc["jp_name"]} : {elem.loc["temperature"]:.1f}°C, {elem.loc["weather"]}\n')
      print(f' - {elem.loc["news_1"]}')
      print(f' - {elem.loc["news_2"]}')
      print(f' - {elem.loc["news_3"]}\n')
   return


def _gen_df_from_db():
   """
   SQLiteデータベースからデータを読み込み、1つのDataFrameに統合し、DataFrameを返す。
   """
   path = f'{os.path.dirname(os.path.abspath(__file__))}\sqlite_db'
   os.chdir(path)

   with sqlite3.connect('city_overview.db') as conn:
      df_cityov = pd.read_sql("SELECT * FROM city_overview", conn)
      df_citynm = pd.read_sql("SELECT * FROM city_name", conn)
      df_weather = pd.read_sql("SELECT * FROM weather_current", conn)
      df_news = pd.read_sql("SELECT * FROM news_latest", conn)

   df_integrated = df_cityov.merge(df_citynm, on="city_id").merge(df_weather, on="weather_id").merge(df_news, on="news_id")
   df_integrated = df_integrated.sort_values(by="overview_id", ascending=True)
   return df_integrated


def get_time_from_df(df_integrated):
   """
   SQLiteデータベースから生成されたDataFrameに対し、str型の単一値としてのtimeを取得する。
   このとき、Series内の全てのtimeが一致していればその値を返し、全一致していなければNoneを返す。
   """
   keep = None
   for i in range(len(df_integrated)):
      latest = df_integrated.iloc[i].loc["date"][:16]
      if keep == None:
         keep = latest
      else:
         if keep == latest:
            continue
         else:
            return None
   return keep