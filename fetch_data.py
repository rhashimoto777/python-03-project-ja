from abc import ABC, abstractmethod
import requests
import pandas as pd
import sqlite3

#________________________________________________________________________________________________________________________
class Data(ABC):
    def __init__(self, API_key):
        self.API_key = API_key

    def _fetch_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error : response.status_code = {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
        

#________________________________________________________________________________________________________________________
class WeatherData(Data):
    def __init__(self, API_key):
        super().__init__(API_key)
    
    def __gen_url(self, city_name):
        openweather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},jp&appid={self.API_key}"
        return openweather_url
    
    def make_df(self, cities):
        dict = []
        for i, city in enumerate(cities):
            city_name = city["en"]
            url = self.__gen_url(city_name)
            data = self._fetch_data(url)
            dict.append({
                'city_id'       : city["city_id"],
                'city_name'     : city_name,                # for debug
                'lat'           : data['coord']['lat'],     # for debug
                'lon'           : data['coord']['lon'],     # for debug
                'weather_id'    : i,
                'temperature'   : data['main']['temp']-273.15,
                'weather'       : data['weather'][0]['description']
            })
        df = pd.DataFrame(dict)
        return(df)

#________________________________________________________________________________________________________________________
class NewsData(Data):
    def __init__(self, API_key):
        super().__init__(API_key)
    
    # def __gen_url(self, city_name):
    #     news_url = f"https://newsapi.org/v2/everything?q='{city_name}'&appid={self.API_key}"
    #     return news_url
    
    def make_df(self, cities):
        dict = []
        for i, city in enumerate(cities):
            city_name = city["jp"]
            # url = self.__gen_url(city_name)
            # data = self._fetch_data(url)

            ENDPOINT = 'https://newsapi.org/v2/everything'
            params = {
                'q': city_name,
                # 'language': 'ja',
                # 'sortBy': 'publishedAt',
                'apiKey': self.API_key
            }
            response = requests.get(ENDPOINT, params=params)
            print(response.status_code)
            data = response.json()
            breakpoint()
        df = pd.DataFrame(dict)
        return(df)
