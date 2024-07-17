import sqlite3
import os
from datetime import datetime

def save_to_sqlite(city_df, weather_df, news_df, db_name='data.db'):
    """
    DataFramesをSQLiteデータベースに保存する
    """
    path = f'{os.path.dirname(os.path.abspath(__file__))}\sqlite_db'
    os.chdir(path)

    with sqlite3.connect('city_overview.db') as sqlite_connection:
        # city_nameテーブルの作成とデータ挿入
        city_df[['city_id', 'jp', 'en']].rename(columns={'jp': 'jp_name', 'en': 'en_name'}).to_sql('city_name', sqlite_connection, if_exists='replace', index=False)

        # weather_currentテーブルの作成とデータ挿入
        weather_df[['weather_id', 'weather', 'temperature']].to_sql('weather_current', sqlite_connection, if_exists='replace', index=False)

        # news_latestテーブルの作成とデータ挿入
        news_df[['news_id', 'news_1', 'news_2', 'news_3']].to_sql('news_latest', sqlite_connection, if_exists='replace', index=False)

        # city_overviewテーブルの作成とデータ挿入
        overview_df = city_df[['city_id']].copy()
        overview_df['date'] = datetime.now()
        overview_df = overview_df.merge(weather_df[['city_id', 'weather_id']], on='city_id')
        overview_df = overview_df.merge(news_df[['city_id', 'news_id']], on='city_id')
        overview_df.to_sql('city_overview', sqlite_connection, if_exists='replace', index=False)

    return
