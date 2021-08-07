from discord_webhook.webhook import DiscordWebhook, DiscordEmbed
import os
from pymongo import MongoClient
import requests
from config import *
import time, random, discord, asyncio


webhook = DiscordWebhook(url=WEBHOOK_URL)  

mainshop = [{"name":"LuckyClover","price":77777,"description":"Work"},
            {"name":"NTD","price":100000000000000000000,"description":"Gaming"},
            {"name":"watch","price":200000,"description":"Sports Car"},
            {"name":"NameColor","price":2000000,"description":"Sports Car"},
            {"name":"BGTutorials","price":99879}
            ]

auth_url = os.getenv("MONGODB_URI")
cluster = MongoClient(auth_url)
db = cluster["Economy"]
cursor = db["Bank"]

async def open_bank(user):
    try:
        post = {"_id": user.id, "現金": 5000, "銀行餘額": 0,  "Roulette":0, "薪資":19000, "who":0, "課稅":0.97, "存款額度":250000,"利息":1.01,"真實的薪資":9000,"利息等階":1,"Rob":0}

        cursor.insert_one(post)

    except:
        pass

async def loading(ctx):
    webhook = await ctx.channel.create_webhook(name = "CC-OSV-WebHook")
    embed= discord.Embed(title="讀取中......", description="請稍等。", color=MAIN_COLOR)
    刪除 = await webhook.send(embed=embed, username = '˚₊ ࣪« 中央銀行 » ࣪ ˖', avatar_url = 'https://imgur.com/csEpNAa.png', allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False),wait=True)

    return 刪除, webhook



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
    user_data = cursor.find({"_id": user.id})

    cols = ["現金", "銀行餘額","Roulette", "薪資", "存款額度", "利息","銀行等階","利息等階","Rob"]
    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data

async def get_國庫():
    user_data = cursor.find({"_id": "國庫"})

    cols = ["當周所得", "餘額"]
    data = []

    for mode in user_data:
        for col in cols:
            data1 = mode[str(col)]

            data.append(data1)

    return data

async def update_bank(user, amount=0, mode="現金"):
    cursor.update_one({"_id": user.id}, {"$inc": {str(mode): amount}})

async def update_set_bank(user, amount=0, mode="現金"):
    cursor.update_one({"_id": user.id}, {"$set": {str(mode): amount}})

async def 利息_data(利息等階):
    if 利息等階 == 1:
        利息等階圖示 ="<:__:852028673363279893>"
        利息等階名稱="普卡 | Classic"
    elif 利息等階 == 2:
        利息等階圖示 ="<:__:852028672760348703>"
        利息等階名稱="金卡 | Gold"
    elif 利息等階 == 3:
        利息等階圖示 ="<:__:852028673280311356>"
        利息等階名稱="白金卡 | Platinum"
    elif 利息等階 == 4:
        利息等階圖示 ="<:__:852028672823394305>"
        利息等階名稱="御璽卡 | Signature"
    elif 利息等階 == 5:
        利息等階圖示 ="<:__:852028672655097856>"
        利息等階名稱="無限卡 | Infinite"
    return [利息等階圖示, 利息等階名稱]

async def 存額_data(new_銀行等階):
    if new_銀行等階 == 1 :
        new_銀行等階圖示 = "<:__:861046014223450122>"
        銀行等階名稱= "木階"
    elif new_銀行等階 >=2 and new_銀行等階 <5:
        new_銀行等階圖示 = "<:__:851791224310595594>"
        銀行等階名稱= "白鐵階"
    elif new_銀行等階 >=5 and new_銀行等階 <50:
        new_銀行等階圖示 = "<:__:861046014336696341>"
        銀行等階名稱= "黃金階"
    elif new_銀行等階 >=50 and new_銀行等階 <100:
        new_銀行等階圖示 = "<:__:861046013792223243>"
        銀行等階名稱= "鑽石階"
    elif new_銀行等階 >=100:
        new_銀行等階圖示 = "<:__:861046014088577024>"
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