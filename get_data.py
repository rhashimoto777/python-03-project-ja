from abc import ABC, abstractmethod
import requests
import pandas as pd
import json
import os

#________________________________________________________________________________________________________________________
class Data(ABC):
    def __init__(self, API_key, is_local_mode):
        self.API_key = API_key
        self.is_local_mode = is_local_mode

    def _get_data(self, city_name):
        """
        APIもしくはLocalのjsonからデータを取得し、dictを返す。
        """
        # 前処理
        json_file_name = self._get_json_file_name(city_name)

        if self.is_local_mode == False:
            # APIからデータを読み込み、読み込んだデータをjsonに保存しておく。
            endpoint, params = self._get_endpoint_and_params(city_name)
            try:
                response = requests.get(endpoint, params)
                if response.status_code == 200:
                    data = response.json()
                    self._dump_to_json(data, json_file_name)
                    return data
                else:
                    print(f"Error : response.status_code = {response.status_code}")
                    return None
            except Exception as e:
                print(f"Error fetching data: {e}")
                return None
        else:
            # jsonからデータを読み込む
            self._chdir_to_json_dump()            
            with open(f"{json_file_name}.json", "r", encoding='utf-8') as file:
                data = json.load(file)
                return data

    
    # @abstractmethod
    def _get_endpoint_and_params(self, city_name):
        pass

    # @abstractmethod
    def _get_json_file_name(self, city_name):
        pass
    
    def _chdir_to_json_dump(self):
        path = f'{os.path.dirname(os.path.abspath(__file__))}\json_dump'
        os.chdir(path)
        return

    def _dump_to_json(self, data, filename):
        self._chdir_to_json_dump()
        if self.is_local_mode == False:
            with open(f"{filename}.json", "w", encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4, sort_keys=True)
        else:
            pass
        return

    # @abstractmethod
    def print_df_for_debug(self, df):
        pass

#________________________________________________________________________________________________________________________
class WeatherData(Data):
    def __init__(self, API_key, is_local_mode):
        super().__init__(API_key, is_local_mode)
    
    def _get_endpoint_and_params(self, city_name):
        openweather_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city_name,
            'apiKey': self.API_key
        }
        return openweather_url, params
    
    def _get_json_file_name(self, city_name):
        return f'weather_{city_name}'
    
    def make_df(self, cities):
        dict = []
        for i, city in enumerate(cities):
            # データを取得する
            city_name = city["en"]
            data = self._get_data(city_name)

            # データのnull値対応は、DataFrame変換後ではなくこの時点で行う。
            # tempはnullだと摂氏に変換できないので、nullの場合は特殊処理を行う。
            # weatherはnull (= Python上だとNone) のときはそのまま表示するため何もしない。
            temp_k = data['main']['temp']
            if temp_k:
                temp_celc = temp_k - 273.15
            else:
                temp_celc = None

            # dictに値を格納する
            dict.append({
                'city_id'     : city["city_id"],
                'weather_id'  : i,
                'temperature' : temp_celc,
                'weather'     : data['weather'][0]['description'],
                '(DEBUG)city_name' : city_name,               # for debug
                '(DEBUG)lat'       : data['coord']['lat'],    # for debug
                '(DEBUG)lon'       : data['coord']['lon']     # for debug
            })
        df = pd.DataFrame(dict)
        return(df)

    def print_df_for_debug(self, df):    
        print("\n######################## debug : weather_df ########################")
        print(df)
        return

#________________________________________________________________________________________________________________________
class NewsData(Data):
    def __init__(self, API_key, is_local_mode):
        super().__init__(API_key, is_local_mode)
    
    def _get_endpoint_and_params(self, city_name):
        news_url = 'https://newsapi.org/v2/everything'
        params = {
            'q': city_name,
            'domains' : 'nhk.or.jp', # 対象記事はNHKに限定する
            'sortBy'  : 'publishedAt',
            'apiKey'  : self.API_key
        }
        return news_url, params

    def _get_json_file_name(self, city_name):
        return f'news_{city_name}'

    def __extract_news(self, data, city_name):
        """
        cityに関連するニュースを抽出し、抽出結果を全て返す。
        """
        max_news_num = 3
        list = []
        for elem in data["articles"]:
            pub_date = elem["publishedAt"][:10]
            source_name = elem["source"]["name"]
            title = elem["title"]

            # 各データがnullではなく、かつtitleに都市名が入っているときのみニュースを抽出する。
            if title and (city_name in title) and pub_date and len(pub_date) == 10 and source_name:
                abstract = f'【{pub_date}】【{source_name}】{title}'
                list.append(abstract)
                if len(list) >= max_news_num:
                    return list

        # もしも十分数記事が取得できなかった場合に、配列外アクセスを防ぐために空の要素を加える
        for i in range(max_news_num - len(list)):
            abstract = ""
            list.append(abstract)
        return list
    
    def make_df(self, cities):
        dict = []
        for i, city in enumerate(cities):
            # データを取得する
            city_name = city["jp"]
            data = self._get_data(city_name)

            # ニュースを選別する。データのクリーニングはこの中で行う。
            news_list = self.__extract_news(data, city_name)

            # dictに値を追加
            dict.append({
                'city_id' : city["city_id"],
                'news_id' : i,
                'news_1'  : news_list[0],
                'news_2'  : news_list[1],
                'news_3'  : news_list[2],
                '(DEBUG)city_name' : city_name
            })
        df = pd.DataFrame(dict)
        return(df)

    def print_df_for_debug(self, df):   
        print("\n######################## debug : news_df ########################")
        for i in range(len(df)):
            elem = df.iloc[i]
            print(f'city_id = {elem.loc["city_id"]}, news_id = {elem.loc["news_id"]}, (DEBUG)city_name = {elem.loc["(DEBUG)city_name"]}')
            print(f' - news_1 : {elem.loc["news_1"]}')
            print(f' - news_2 : {elem.loc["news_2"]}')
            print(f' - news_3 : {elem.loc["news_3"]}\n')
        return

