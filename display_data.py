import pandas as pd
from sqlalchemy import create_engine

def display_data(db_name='data.db'):
    """
    SQLiteデータベースからデータを読み込み、結合して表示する
    """
    engine = create_engine(f'sqlite:///{db_name}', echo=False)
    sqlite_connection = engine.connect()

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

    sqlite_connection.close()


    # SELECT cn.jp_name AS city_name, wc.temperature, wc.weather, 
    #        nl.news_1, nl.news_2, nl.news_3
    # FROM city_overview co
    # JOIN city_name cn ON co.city_id = cn.city_id
    # JOIN weather_current wc ON co.weather_id = wc.weather_id
    # JOIN news_latest nl ON co.news_id = nl.news_id
