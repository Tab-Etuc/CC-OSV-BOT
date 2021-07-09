from discord_webhook.webhook import DiscordWebhook, DiscordEmbed
import os, json
from pymongo import MongoClient
import requests
from config import *
import time
import random

with open('bot_info.json','r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
    WEBHOOK_URL = jdata["WEBHOOK_URL"]

mainshop = [{"name":"LuckyClover","price":77777,"description":"Work"},
            {"name":"NTD","price":100000000000000000000,"description":"Gaming"},
            {"name":"watch","price":200000,"description":"Sports Car"},
            {"name":"NameColor","price":2000000,"description":"Sports Car"},
            {"name":"BGTutorials","price":99879}
            ]

auth_url = os.getenv("MONGODB_URI")

async def open_bank(user):
    cluster = MongoClient(auth_url)
    db = cluster["Economy"]

    cursor = db["Bank"]

    try:
        post = {"_id": user.id, "現金": 5000, "銀行餘額": 0,  "Roulette":0, "薪資":19000, "who":0, "課稅":0.97, "存款額度":250000,"利息":1.01,"真實的薪資":9000,"利息等階":1,"Rob":0}

        cursor.insert_one(post)

    except:
        pass

async def loading():
    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/859633422498398288/5JVnexiCnP3BIk-kLPuAk4xDqadplNzgv-85zyS25poVDjhFjPwXz1CX0SDkbUlkcSwb')
    embed= DiscordEmbed(title="讀取中......", description="請稍等。", color=MAIN_COLOR)
    webhook.add_embed(embed)
    刪除 = webhook.execute(embed)
    return 刪除

async def open_account(user):

      users = await get_bag_data()

      if str(user.id) in users:
          return False
      else:
          users[str(user.id)] = {}


      requests.put("https://api.jsonstorage.net/v1/json/828f40b5-a226-456f-ab67-bce869cd1ad9", json = {users:f})

      return True

async def get_bag_data():
  r = requests.get('https://api.jsonstorage.net/v1/json/828f40b5-a226-456f-ab67-bce869cd1ad9')
  return r.json()

async def buy_this(user,item_name,amount,new):
  item_name = item_name.lower()
  name_ = None
  for item in mainshop:
      name = item["name"].lower()
      if name == item_name:
          name_ = name
          price = item["price"]
          break
  if name_ == None:
      return [False,1]
  users = await get_bag_data()

  bal_data = await get_bank_data(user)
  bal = bal_data[0]
  cost = price*amount


  if bal < cost:
      return [False,2]
            
  try:
    index = 0
    t = None
    for thing in users[str(new.id)]["bag"]:
        n = thing["item"]
        if n == item_name:
                """old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(new.id)]["bag"][index]["amount"] = new_amt
                t = 1"""
                return [False,3]
                break
        index+=1 
    if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(new.id)]["bag"].append(obj)
  except:
        obj = {"item":item_name , "amount" : amount}
        users[str(new.id)]["bag"] = [obj]        
            
  requests.put("https://api.jsonstorage.net/v1/json/828f40b5-a226-456f-ab67-bce869cd1ad9", json = users)

  await update_bank(user,-1*cost,"現金")
  
  return [True,"Worked"]

async def get_bank_data(user):
    cluster = MongoClient(auth_url)
    db = cluster["Economy"]

    cursor = db["Bank"]

    user_data = cursor.find({"_id": user.id})

    cols = ["現金", "銀行餘額","Roulette", "薪資", "存款額度", "利息","銀行等階","利息等階","Rob"]
    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data

async def get_國庫():
    cluster = MongoClient(auth_url)
    db = cluster["Economy"]

    cursor = db["Bank"]

    user_data = cursor.find({"_id": "國庫"})

    cols = ["當周所得", "餘額"]
    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data

async def update_bank(user, amount=0, mode="現金"):
    cluster = MongoClient(auth_url)
    db = cluster["Economy"]

    cursor = db["Bank"]

    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})

async def update_set_bank(user, amount=0, mode="現金"):
    cluster = MongoClient(auth_url)
    db = cluster["Economy"]

    cursor = db["Bank"]

    cursor.update_one({"_id": user.id}, {"$set": {str(mode): amount}})

async def 利息_data(利息等階):
    if 利息等階 == 1:
        利息等階圖示 ="<:__:861522025008463883>"
        利息等階名稱="普卡 | Classic"
    elif 利息等階 == 2:
        利息等階圖示 ="<:__:861522025000468501>"
        利息等階名稱="金卡 | Gold"
    elif 利息等階 == 3:
        利息等階圖示 ="<:__:861522025704849408>"
        利息等階名稱="白金卡 | Platinum"
    elif 利息等階 == 4:
        利息等階圖示 ="<:__:861522025378349096>"
        利息等階名稱="御璽卡 | Signature"
    elif 利息等階 == 5:
        利息等階圖示 ="<:__:861522024999419914>"
        利息等階名稱="無限卡 | Infinite"
    return [利息等階圖示, 利息等階名稱]

async def 存額_data(new_銀行等階):
    if new_銀行等階 == 1 :
        new_銀行等階圖示 = "<:woof:861185764786962442>"
        銀行等階名稱= "木階"
    elif new_銀行等階 >=2 and new_銀行等階 <5:
        new_銀行等階圖示 = "<:iron:861474687917359114>"
        銀行等階名稱= "白鐵階"
    elif new_銀行等階 >=5 and new_銀行等階 <50:
        new_銀行等階圖示 = "<:gold:861186184340045844>"
        銀行等階名稱= "黃金階"
    elif new_銀行等階 >=50 and new_銀行等階 <100:
        new_銀行等階圖示 = "<:diamond:861185706336845834>"
        銀行等階名稱= "鑽石階"
    elif new_銀行等階 >=100:
        new_銀行等階圖示 = "<:emerald:861185706370400266>"
        銀行等階名稱= "翡翠階"
    return [new_銀行等階圖示, 銀行等階名稱]


async def roulette(name):
    users = await get_bank_data(name)
    timer = users[8] 
    現金 = users[1]
    now_time = int(time.time())

    timeleft = int(time.time() - timer)
    timeleft = 86400 - timeleft

    if timeleft > 0:
        typeT = '秒'
        if timeleft > 60:
            timeleft = timeleft // 60 + 1
            typeT = '分鐘'
            if timeleft > 60:
                timeleft = timeleft // 60
                typeT = '小時'
        webhook = DiscordWebhook(url=WEBHOOK_URL, content='你仍須等待{}{}!'.format(timeleft, typeT))
        webhook.execute()

    num = random.randint(1, 6)
    if num == 1:
        await update_bank(name,現金*6)
        await update_set_bank(name,now_time,"Roulette")
        webhook = DiscordWebhook(url=WEBHOOK_URL, content='你安全了！你將你的現金翻了六倍！')
        webhook.execute()
    else:
        await update_set_bank(name,now_time,"Roulette")
        await update_set_bank(name)
        webhook = DiscordWebhook(url=WEBHOOK_URL, content='BOOM! 你死了。 :(')
        webhook.execute()