from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://t.weather.sojson.com/api/weather/city/101180301"
  res = requests.get(url).json()
  weather = res['data']
  return weather['forecast'][0]['high'],weather['forecast'][0]['low'],weather['forecast'][0]['type'],weather['forecast'][0]['week'],weather['forecast'][0]['ymd'],weather['forecast'][0]['notice']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

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
# wea, temperature, low, high, airQuality = get_weather()
high,low,type,week,ymd,notice = get_weather()
data = {
    "week": {"value": week, "color": get_random_color()},
    "low":{"value":low, "color":get_random_color()},
    "high":{"value":high, "color":get_random_color()},
    "type":{"value":type, "color":get_random_color()},
    "ymd": {"value": ymd, "color": get_random_color()},
    "notice": {"value": notice, "color": get_random_color()},
    "love_days":{"value":get_count(), "color":get_random_color()},
    "birthday_left":{"value":get_birthday(), "color":get_random_color()},
    "words":{"value":get_words(), "color":get_random_color()}
}
res = wm.send_template(user_id, template_id, data)
ress = wm.send_template("oPQbt6rUeEafvH8D1606d8j0_z24", template_id, data)
print(res)
