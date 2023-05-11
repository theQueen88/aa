from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
from requests.packages import urllib3
import os
import random
import schedule
import time
 
today = datetime.now()
 
start_date = "2023-03-27"  #你们恋爱开始的时间开始时间
city = "101190704"         #城市id 具体的可以在https://www.sojson.com/blog/305.html查询
gyjbirthday = "08-20"  # 两个人的生日生日
zcbirthday = "10-22"  #生日
app_id = "wx85f226df68a65292" #微信测试的app_id
app_secret = "6d07756f1a35cc0c0b0a18417a58b0aa" #微信测试的app_secret
user_id = "oPQbt6nQb3L2qwE-_Q1bSvEcMyXs"        #生成的user_id 让你的女朋友扫码 显示出来的id
template_id = "NJgwDso2e3b22J6VXxyGso4x1lluj6tiZXj0Q0W7GuU" #模板id
 
# 返回  当天最高最低气温 当天天气情况 
def get_weather():
  url = "http://t.weather.sojson.com/api/weather/city/" + city
  res = requests.get(url).json()
  weather = res['data']
  return weather['forecast'][0]['high'],weather['forecast'][0]['low'],weather['forecast'][0]['type'],weather['forecast'][0]['week'],weather['forecast'][0]['ymd']
 
# 星座运势
def get_lucky():
  url = "http://web.juhe.cn:8080/constellation/getAll?consName=狮子座&type=today&key=4a11bbcbf089edaf14c2d9bdb80c2ec4"
  res = requests.get(url).json()
  return res['color'],res['summary']
 
# 新闻
def get_info():
  url = "http://v.juhe.cn/toutiao/index?type=yule&key=d268884b9b07c0eb9d6093dc54116018"
  res = requests.get(url).json()['result']
  info = res['data'][0]['title']
  return info
 
# 获取历史今天
def get_history():
  url = "https://api.oick.cn/lishi/api.php"
  res= requests.get(url).json()
  history = res['result'][0]
  return history['date'],history['title']
 
# 返回 在一起的天数
def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days
 
# 距离下个生日还有多久
def get_birthday():
  gyjnext = datetime.strptime(str(date.today().year) + "-" + gyjbirthday, "%Y-%m-%d")
  if gyjnext < datetime.now():
    gyjnext = gyjnext.replace(year=gyjnext.year + 1)
 
  zcnext = datetime.strptime(str(date.today().year) + "-" + zcbirthday, "%Y-%m-%d")
  if zcnext < datetime.now():
    zcnext = zcnext.replace(year=zcnext.year + 1)
  return (gyjnext - today).days,(zcnext - today).days
 
# 生成有趣的文案
def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']
 
# 随机颜色
def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)
 
def run():
  client = WeChatClient(app_id, app_secret)
  wm = WeChatMessage(client)
  high,low,type,week,ymd = get_weather()
  gyj,zc = get_birthday()
  color,summary = get_lucky()
  date,title = get_history()
  info = get_info()
 
  data = {
    "info": {"value": info, "color": get_random_color()},
    "date": {"value": date, "color": get_random_color()},
    "title": {"value": title, "color": get_random_color()},
    "color": {"value": color, "color": get_random_color()},
    "summary": {"value": summary, "color": get_random_color()},
    "week": {"value": week, "color": get_random_color()},
    "ymd": {"value": ymd, "color": get_random_color()},
    "type":{"value":type, "color":get_random_color()},
    "high": {"value": high, "color": get_random_color()},
    "low": {"value": low, "color": get_random_color()},
    "love_days":{"value":get_count(), "color":get_random_color()},
    "birthdaygyj":{"value":gyj, "color":get_random_color()},
    "birthdayzc": {"value": zc, "color": get_random_color()},
    "words":{"value":get_words(), "color":get_random_color()}
  }
  # 发送消息
  res = wm.send_template(user_id, template_id, data)
  if res['errmsg'] == 'ok':
    print(ymd + '消息发送成功')
# run()
# 定时器 每天什么时候发送消息
schedule.every().day.at("11:00").do(run)
while True:
    schedule.run_pending()
    time.sleep(1)
 
