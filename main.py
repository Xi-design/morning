from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
#start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
key = os.environ["WEA_KEY"]

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


# def get_weather():
#   url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
#   res = requests.get(url).json()
#   weather = res['data']['list'][0]
#   return weather['weather'], math.floor(weather['temp'])
def get_weather():
    url = "https://devapi.qweather.com/v7/weather/3d?location=101190113&lang=zh&unit=m&key=" + key
    res = requests.get(url).json()
    weather_today = res['daily'][0]
    weather_tomorrow = res['daily'][1]
    weather_after_tomorrow = res['daily'][2]
    return weather_today,weather_tomorrow,weather_after_tomorrow,res['fxLink']

# def get_count():
#   delta = today - datetime.strptime(start_date, "%Y-%m-%d")
#   return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
weather_today,weather_tomorrow,weather_after_tomorrow,linkdetail = get_weather()
# data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
data = {"weather":{"value":weather_today['textDay']},"MaxTemp":{"value":weather_today['tempMax']},"MinTemp":{"value":weather_today['tempMin']},"Featurewea":{"value":weather_tomorrow['fxDate'] + ":" +weather_tomorrow['textDay'] + ";" + weather_after_tomorrow['fxDate'] + ":" + weather_after_tomorrow['textDay']},"Featuretemp":{"value":weather_tomorrow['tempMax'] + "°C;" + weather_after_tomorrow['tempMax']+"°C."},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(),"color":get_random_color()},"links":{"value":linkdetail}}
res = wm.send_template(user_id, template_id, data)
print(res)
