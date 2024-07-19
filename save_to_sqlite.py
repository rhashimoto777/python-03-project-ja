import sqlite3
import os
from datetime import datetime

def save_to_sqlite(city_df, weather_df, news_df, db_name='city_overview.db'):
    """
    DataFramesをSQLiteデータベースに保存する
    """
    path = f'{os.path.dirname(os.path.abspath(__file__))}/sqlite_db'
    os.makedirs(path, exist_ok=True)
    os.chdir(path)

    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # 外部キー制約を有効にする
        cursor.execute('PRAGMA foreign_keys = ON;')
                
        # 既存のテーブルを削除する
        cursor.execute('DROP TABLE IF EXISTS city_overview')
        cursor.execute('DROP TABLE IF EXISTS city_name')
        cursor.execute('DROP TABLE IF EXISTS weather_current')
        cursor.execute('DROP TABLE IF EXISTS news_latest')

        # テーブルの作成（外部キー制約付き）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_overview (
                overview_id INTEGER PRIMARY KEY,
                date TIMESTAMP,
                city_id INTEGER,
                weather_id INTEGER,
                news_id INTEGER,
                FOREIGN KEY(city_id) REFERENCES city_name(city_id),
                FOREIGN KEY(weather_id) REFERENCES weather_current(weather_id),
                FOREIGN KEY(news_id) REFERENCES news_latest(news_id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS city_name (
                city_id INTEGER PRIMARY KEY,
                jp_name TEXT,
                en_name TEXT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_current (
                weather_id INTEGER PRIMARY KEY,
                weather TEXT,
                temperature INTEGER
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_latest (
                news_id INTEGER PRIMARY KEY,
                news_1 TEXT,
                news_2 TEXT,
                news_3 TEXT
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
        city_df[['city_id', 'jp', 'en']].rename(columns={'jp': 'jp_name', 'en': 'en_name'}).to_sql('city_name', conn, if_exists='append', index=False)
        weather_df[['weather_id', 'weather', 'temperature']].to_sql('weather_current', conn, if_exists='append', index=False)
        news_df[['news_id', 'news_1', 'news_2', 'news_3']].to_sql('news_latest', conn, if_exists='append', index=False)

        overview_df = city_df[['city_id']].copy()
        overview_df['overview_id'] = overview_df[['city_id']]+1 # 1から始まるようにするために+1する
        overview_df['date'] = datetime.now()
        overview_df = overview_df.merge(weather_df[['weather_id']], left_index=True, right_index=True)
        overview_df = overview_df.merge(news_df[['news_id']], left_index=True, right_index=True)
        overview_df.to_sql('city_overview', conn, if_exists='append', index=False)

        # 外部キー制約のチェックを再度有効にする
        cursor.execute('PRAGMA foreign_keys = ON;')

    return


