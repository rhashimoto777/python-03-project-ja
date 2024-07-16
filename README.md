# python-03-project-ja

## 作成するデータ構造

https://databasediagram.com/app

```
city_overview
-
date datetime64
city_id int PK
weather_id int PK
news_id int PK

city_name
-
city_id int FK > city_overview.city_id
jp_name str
en_name int

weather_current
-
weather_id int FK > city_overview.weather_id
weather str
temparature int

news_today
-
news_id int FK > city_overview.news_id
news_headline_1 str
news_headline_2 str
news_headline_3 str
```