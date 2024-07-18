import pandas as pd
import sqlite3
import os

def display_data(db_name='data.db'):
    """
    SQLiteデータベースからデータを読み込み、結合して表示する
    """
    path = f'{os.path.dirname(os.path.abspath(__file__))}\sqlite_db'
    os.chdir(path)

    with sqlite3.connect('city_overview.db') as sqlite_connection:
       query = """
       SELECT cn.jp_name AS city_name, wc.temperature, wc.weather, 
              nl.news_1, nl.news_2, nl.news_3
       FROM city_overview co
       JOIN city_name cn ON co.city_id = cn.city_id
       JOIN weather_current wc ON co.weather_id = wc.weather_id
       JOIN news_latest nl ON co.news_id = nl.news_id
       """
       result_df = pd.read_sql(query, sqlite_connection)
       print(result_df)
    return
