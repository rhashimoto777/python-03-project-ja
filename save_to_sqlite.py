import sqlite3
import os
from datetime import datetime
import pandas as pd

def save_to_sqlite(city_df, weather_df, news_df, db_name='data1.db'):
    """
    DataFramesをSQLiteデータベースに保存する
    """
    path = f'{os.path.dirname(os.path.abspath(__file__))}/sqlite_db'
    os.makedirs(path, exist_ok=True)
    os.chdir(path)

    with sqlite3.connect(db_name) as sqlite_connection:
        cursor = sqlite_connection.cursor()
        
        # 外部キー制約を有効にする
        cursor.execute('PRAGMA foreign_keys = ON;')

        # テーブルの作成（外部キー制約付き）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_overview (
                date TIMESTAMP,
                city_id INTEGER,
                weather_id INTEGER,
                news_id INTEGER,
                PRIMARY KEY(city_id, weather_id, news_id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_name (
                city_id INTEGER PRIMARY KEY,
                jp_name TEXT,
                en_name TEXT,
                FOREIGN KEY(city_id) REFERENCES city_overview(city_id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_current (
                weather_id INTEGER PRIMARY KEY,
                weather TEXT,
                temperature INTEGER,
                FOREIGN KEY(weather_id) REFERENCES city_overview(weather_id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_latest (
                news_id INTEGER PRIMARY KEY,
                news_1 TEXT,
                news_2 TEXT,
                news_3 TEXT,
                FOREIGN KEY(news_id) REFERENCES city_overview(news_id)
            );
        ''')

        # 外部キー制約のチェックを一時的に無効にする
        cursor.execute('PRAGMA foreign_keys = OFF;')

        # 既存のデータを削除（適切な順序で）
        cursor.execute('DELETE FROM city_overview')
        cursor.execute('DELETE FROM city_name')
        cursor.execute('DELETE FROM weather_current')
        cursor.execute('DELETE FROM news_latest')


        # データの挿入
        city_df[['city_id', 'jp', 'en']].rename(columns={'jp': 'jp_name', 'en': 'en_name'}).to_sql('city_name', sqlite_connection, if_exists='append', index=False)
        weather_df[['weather_id', 'weather', 'temperature']].to_sql('weather_current', sqlite_connection, if_exists='append', index=False)
        news_df[['news_id', 'news_1', 'news_2', 'news_3']].to_sql('news_latest', sqlite_connection, if_exists='append', index=False)

        overview_df = city_df[['city_id']].copy()
        overview_df['date'] = datetime.now()
        overview_df = overview_df.merge(weather_df[['weather_id']], left_index=True, right_index=True)
        overview_df = overview_df.merge(news_df[['news_id']], left_index=True, right_index=True)
        overview_df.to_sql('city_overview', sqlite_connection, if_exists='append', index=False)

        # 外部キー制約のチェックを再度有効にする
        cursor.execute('PRAGMA foreign_keys = ON;')

    return


