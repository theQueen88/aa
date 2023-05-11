from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import random
 
today = datetime.now()     # 获取今日日期
start_date = "2023-03-27"  # 恋爱开始时间
city = "101190704"         # 城市天气查询的id ,根据自己城市查询城市ID
birthday = "10-22"         # 出生日期
app_id = "wx85f226df68a65292" # app_id
app_secret = "6d07756f1a35cc0c0b0a18417a58b0aa"   # appsecret
user_id = ["oPQbt6nQb3L2qwE-_Q1bSvEcMyXs"]        # user_id 关注的用户微信ID
template_id = "NTn32uewJaOPSH58-v_vwt9HlpsRV-LflSjV_h6ZiSo"  # 生成的模板id， 新建的ID
 
def get_weather():
  url = "http://t.weather.sojson.com/api/weather/city/" + city
  res = requests.get(url).json()
  citys = res['cityInfo']
  weather = res['data']['forecast']
  return weather, citys

def get_lucky():
  url = "http://web.juhe.cn:8080/constellation/getAll?consName=天秤座&type=today&key=4a11bbcbf089edaf14c2d9bdb80c2ec4"
  res = requests.get(url).json()
  return res['color'],res['summary']
 
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
color,summary = get_lucky()
weather_list, city_list = get_weather()
# 划分天气信息
print(weather_list)
type = weather_list[0]['type']   # 天气类型
tep_high = weather_list[0]['high'] # 高温
tep_low = weather_list[0]['low']   # 低温
notice = weather_list[0]['notice']  # 提示信息
week = weather_list[0]['week']  # 星期几
ymd = weather_list[0]['ymd']  # 年月日
# 划分城市
parent = city_list['parent']
citys = city_list['city']
 
data = {"parent":{"value":parent, "color": get_random_color()},
        "city":{"value":citys, "color": get_random_color()},
        "type":{"value":type, "color": get_random_color()},
         "color": {"value": color, "color": get_random_color()},
         "summary": {"value": summary, "color": get_random_color()},
        "tep_high":{"value":tep_high, "color": get_random_color()},
        "tep_low":{"value":tep_low, "color": get_random_color()},
        "notice":{"value":notice, "color": get_random_color()},
        "week":{"value":week, "color": get_random_color()},
        "ymd":{"value":ymd, "color": get_random_color()},
        "love_days":{"value":get_count(), "color": get_random_color()},
        "birthday_left":{"value":get_birthday(), "color": get_random_color()},
        "words":{"value":get_words(), "color": get_random_color()}}
 
# 群发消息
for i in range(len(user_id)):
  res = wm.send_template(user_id[i], template_id, data)
  print(res)
 
 
 
