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
        json_file_name = self._get_json_file_name(city_name)

        if self.is_local_mode == False:
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
            self._chdir_to_json_dump()            
            with open(f"{json_file_name}.json", "r") as file:
                data = json.load(file)
                return data

    
    # @abstractmethod
    def _get_endpoint_and_params(self, city_name):
        pass

    # @abstractmethod
    def _get_json_file_name(self, city_name):
        return city_name
    
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
            city_name = city["en"]
            data = self._get_data(city_name)
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
    def __init__(self, API_key, is_local_mode):
        super().__init__(API_key, is_local_mode)
    
    def _get_endpoint_and_params(self, city_name):
        news_url = 'https://newsapi.org/v2/everything'
        params = {
            'q': city_name,
            'sortBy': 'popularity',
            'from'  : '2024-07-09',
            'apiKey': self.API_key
        }
        return news_url, params

    def _get_json_file_name(self, city_name):
        return f'news_{city_name}'
    
    def make_df(self, cities):
        dict = []
        for i, city in enumerate(cities):
            city_name = city["jp"]
            data = self._get_data(city_name)
            
            dict.append({
                'city_id'       : city["city_id"],
                'city_name'     : city_name,                # for debug
                'news_id'       : i,
                'news_1'        : "(TBD)NewsTitle1",
                'news_2'        : "(TBD)NewsTitle2",
                'news_3'        : "(TBD)NewsTitle1",

            })
        df = pd.DataFrame(dict)
        return(df)
